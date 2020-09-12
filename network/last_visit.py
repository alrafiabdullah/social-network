from django.utils.timezone import now


class SetLastVisitMiddleWare(object):
    def process_response(self, request, response):
        if request.user.is_authenticated():
            current_user = User.objects.filter(pk=request.user.pk)
            current_user.last_visit = now()
            current_user.save()
        return response
