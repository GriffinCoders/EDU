from rest_framework.throttling import UserRateThrottle


class StudentRateThrottle(UserRateThrottle):
    scope = 'student'
