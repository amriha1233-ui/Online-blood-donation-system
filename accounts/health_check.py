"""
Health check view for monitoring and load balancers
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
import os


def health_check(request):
    """
    Health check endpoint that verifies:
    - Database connectivity
    - Redis connectivity
    - Application status
    
    Returns:
        200 OK - All systems operational
        503 Service Unavailable - One or more services down
    """
    
    status = {
        "status": "healthy",
        "database": {"status": "error"},
        "cache": {"status": "error"},
        "services": {
            "donors": {"count": 0},
            "hospitals": {"count": 0},
            "requests": {"count": 0},
        }
    }
    
    http_status = 200
    
    # Check Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status["database"]["status"] = "ok"
    except Exception as e:
        status["database"]["status"] = "error"
        status["database"]["error"] = str(e)
        http_status = 503
    
    # Check Redis/Cache
    try:
        cache.set("health_check", "ok", 10)
        result = cache.get("health_check")
        if result == "ok":
            status["cache"]["status"] = "ok"
        else:
            status["cache"]["status"] = "error"
            http_status = 503
    except Exception as e:
        status["cache"]["status"] = "error"
        status["cache"]["error"] = str(e)
        # Don't fail health check if cache is unavailable
        # (graceful degradation)
    
    # Get model counts if database is working
    if status["database"]["status"] == "ok":
        try:
            from donors.models import Donor
            from hospitals.models import Hospital
            from blood_requests.models import BloodRequest
            
            status["services"]["donors"]["count"] = Donor.objects.count()
            status["services"]["hospitals"]["count"] = Hospital.objects.count()
            status["services"]["requests"]["count"] = BloodRequest.objects.count()
        except Exception as e:
            status["services"]["error"] = str(e)
    
    # Overall status
    if http_status != 200:
        status["status"] = "unhealthy"
    
    return JsonResponse(status, status=http_status)


def readiness_check(request):
    """
    Readiness check - application is ready to accept traffic
    """
    from django.apps import apps
    
    status = {
        "ready": True,
        "checks": {
            "database": False,
            "apps": False,
            "migrations": False,
        }
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status["checks"]["database"] = True
    except Exception:
        status["checks"]["database"] = False
        status["ready"] = False
    
    # Check apps loaded
    status["checks"]["apps"] = apps.ready
    if not apps.ready:
        status["ready"] = False
    
    # Check migrations applied
    from django.db.migrations.executor import MigrationExecutor
    try:
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.disk_migrations)
        status["checks"]["migrations"] = len(plan) == 0
        if len(plan) > 0:
            status["ready"] = False
    except Exception:
        status["checks"]["migrations"] = False
        status["ready"] = False
    
    http_status = 200 if status["ready"] else 503
    return JsonResponse(status, status=http_status)
