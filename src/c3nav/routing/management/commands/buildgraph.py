from django.core.management.base import BaseCommand

from c3nav.mapdata.render import render_all_levels
from c3nav.routing.graph import Graph


class Command(BaseCommand):
    help = 'build the routing graph'

    def handle(self, *args, **options):
        graphbuilder = Graph()
        graphbuilder.build()
