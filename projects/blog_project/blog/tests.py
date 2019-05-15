from django.test import TestCase
from django.db import models

from .models import Post


class ArchivesTests(TestCase):
    def test_was_archives_correct(self):
        # date = [[2017, 8], [2017, 10], [2018, 1], [2018, 7], [2019, 5], [2019, 12]]
        # results = [1, 0, 0, 1, 2, 0]
        # for i in range(len(date)):
        #     archives_list = Post.objects.filter(created_time__year=date[i][0],
        #                                         created_time__month=date[i][1])
        #     self.assertIs(len(archives_list), results[i])

        archives_list = Post.objects.filter(created_time__year=2019,
                                            created_time__month=5)
        self.assertIs(len(archives_list), 2)
