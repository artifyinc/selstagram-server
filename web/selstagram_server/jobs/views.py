# Create your views here.
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from jobs.models import CrawlJob, BaseJob
from jobs.serializers import CrawlJobSerializer
from selsta101.management.commands.crawl import Command as CrawlCommand


class CrawlJobViewSet(viewsets.ModelViewSet):
    serializer_class = CrawlJobSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    queryset = CrawlJob.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(status=BaseJob.JobStatus.IN_PROGRESS)

        try:
            headers = self.get_success_headers(serializer.data)

            tag = request.data.get('tag', None)
            limit_count = request.data.get('limit_count', None)

            if limit_count:
                limit_count = int(limit_count)

            CrawlCommand.crawl(limit_count, tag, None)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            error_data = serializer.data
            error_data.update({'exception': str(e)})
            return Response(error_data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            headers=headers)
