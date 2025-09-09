from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from user.models import User
from user.serializers import PublicUserSerializer
from .models import UserFilter
from .serializers import UserFilterSerializer

PRIORITY_FIELDS = ["gender", "nation", "state", "city", "district", "mandal", "village"]

def apply_priority_filters(qs, params):
    """
    Apply LinkedIn-like priority:
    gender > nation > state > city > district > mandal > village
    If a level has no results, loosen to the next level (but never break gender if provided).
    """
    gender = params.get("gender")
    if gender:
        qs = qs.filter(gender=gender)

    constrained_qs = qs
    for f in PRIORITY_FIELDS[1:]:  # skip gender
        val = params.get(f)
        if not val:
            continue
        narrowed = constrained_qs.filter(**{f: val})
        if narrowed.exists():
            constrained_qs = narrowed
    return constrained_qs

# -----------------------
# SavedFilter Functional View
# -----------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def saved_filter_view(request):
    """
    GET -> fetch current user's saved filter
    POST -> create/update saved filter
    """
    uf, _ = UserFilter.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        return Response(UserFilterSerializer(uf).data)

    elif request.method == 'POST':
        serializer = UserFilterSerializer(uf, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# -----------------------
# FilterUsers Functional View
# -----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_users_view(request):
    """
    Returns users ordered by best match according to priority logic.
    """
    params = request.query_params.copy()

    only_opp = params.get("only_opposite") in ("1", "true", "True")
    if only_opp:
        params["gender"] = "female" if request.user.gender == "male" else "male"

    qs = User.objects.exclude(id=request.user.id)

    # Apply priority constraint
    constrained = apply_priority_filters(qs, params)

    # Ranking: count how many priority fields match
    def match_score(u):
        score = 0
        for f in PRIORITY_FIELDS:
            val = params.get(f)
            if val and getattr(u, f, None) == val:
                score += 1
        return score

    users_list = list(constrained)
    users_list.sort(key=match_score, reverse=True)

    data = PublicUserSerializer(users_list, many=True).data
    return Response(data, status=status.HTTP_200_OK)
