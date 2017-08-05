from django.db import models
from django.utils.translation import ugettext_lazy as _
from shapely.ops import cascaded_union

from c3nav.mapdata.fields import GeometryField
from c3nav.mapdata.models import Level
from c3nav.mapdata.models.access import AccessRestrictionMixin
from c3nav.mapdata.models.geometry.base import GeometryMixin
from c3nav.mapdata.models.locations import SpecificLocation
from c3nav.mapdata.utils.geometry import assert_multilinestring, assert_multipolygon


class LevelGeometryMixin(GeometryMixin):
    level = models.ForeignKey('mapdata.Level', on_delete=models.CASCADE, verbose_name=_('level'))

    class Meta:
        abstract = True

    def get_geojson_properties(self, *args, instance=None, **kwargs) -> dict:
        result = super().get_geojson_properties(*args, **kwargs)
        result['level'] = self.level_id
        if hasattr(self, 'get_color'):
            color = self.get_color(instance=instance)
            if color:
                result['color'] = color
        if hasattr(self, 'opacity'):
            result['opacity'] = self.opacity
        return result

    def _serialize(self, level=True, **kwargs):
        result = super()._serialize(**kwargs)
        if level:
            result['level'] = self.level_id
        return result


class Building(LevelGeometryMixin, models.Model):
    """
    The outline of a building on a specific level
    """
    geometry = GeometryField('polygon')

    class Meta:
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')
        default_related_name = 'buildings'


class Space(SpecificLocation, LevelGeometryMixin, models.Model):
    """
    An accessible space. Shouldn't overlap with spaces on the same level.
    """
    geometry = GeometryField('polygon')
    outside = models.BooleanField(default=False, verbose_name=_('only outside of building'))

    class Meta:
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')
        default_related_name = 'spaces'


class Door(AccessRestrictionMixin, LevelGeometryMixin, models.Model):
    """
    A connection between two spaces
    """
    geometry = GeometryField('polygon')

    class Meta:
        verbose_name = _('Door')
        verbose_name_plural = _('Doors')
        default_related_name = 'doors'


class AltitudeArea(LevelGeometryMixin, models.Model):
    """
    An altitude area
    """
    geometry = GeometryField('polygon')
    altitude = models.DecimalField(_('altitude'), null=False, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = _('Altitude Area')
        verbose_name_plural = _('Altitude Areas')
        default_related_name = 'altitudeareas'

    @classmethod
    def recalculate(cls):
        # collect location areas
        all_areas = []
        for level in Level.objects.prefetch_related('buildings', 'doors', 'spaces', 'spaces__columns',
                                                    'spaces__obstacles', 'spaces__lineobstacles', 'spaces__holes',
                                                    'spaces__stairs', 'spaces__altitudemarkers'):
            areas = []
            stairs = []
            spaces = {}

            # collect all accessible areas on this level
            buildings_geom = cascaded_union(tuple(building.geometry for building in level.buildings.all()))
            for space in level.spaces.all():
                if space.outside:
                    space.geometry = space.geometry.difference(buildings_geom)
                spaces[space.pk] = space
                area = space.geometry
                buffered = space.geometry.buffer(0.0001)
                remove = cascaded_union(tuple(c.geometry for c in space.columns.all()) +
                                        tuple(o.geometry for o in space.obstacles.all()) +
                                        tuple(o.buffered_geometry for o in space.lineobstacles.all()) +
                                        tuple(h.geometry for h in space.holes.all()))
                areas.extend(assert_multipolygon(space.geometry.difference(remove)))
                for stair in space.stairs.all():
                    substairs = tuple(assert_multilinestring(stair.geometry.intersection(buffered).difference(remove)))
                    for substair in substairs:
                        substair.space = space.pk
                    stairs.extend(substairs)

            areas = assert_multipolygon(cascaded_union(areas+list(door.geometry for door in level.doors.all())))
            areas = [AltitudeArea(geometry=area, level=level) for area in areas]

            space_areas = {space.pk: [] for space in level.spaces.all()}

            # assign spaces to areas
            for area in areas:
                area.spaces = set()
                area.connected_to = []
                for space in level.spaces.all():
                    if area.geometry.intersects(space.geometry):
                        area.spaces.add(space.pk)
                        space_areas[space.pk].append(area)

            # divide areas using stairs
            for stair in stairs:
                for area in space_areas[stair.space]:
                    if not stair.intersects(area.geometry):
                        continue

                    divided = assert_multipolygon(area.geometry.difference(stair.buffer(0.0001)))
                    if len(divided) > 2:
                        raise ValueError
                    area.geometry = divided[0]
                    if len(divided) == 2:
                        new_area = AltitudeArea(geometry=divided[1], level=level)
                        new_area.spaces = set()
                        new_area.connected_to = [area]
                        area.connected_to.append(new_area)
                        areas.append(new_area)
                        original_spaces = area.spaces
                        if len(area.spaces) == 1:
                            new_area.spaces = area.spaces
                            space_areas[next(iter(area.spaces))].append(new_area)
                        else:
                            for subarea in (area, new_area):
                                spaces_before = subarea.spaces
                                subarea.spaces = set(space for space in original_spaces
                                                     if spaces[space].geometry.intersects(subarea.geometry))
                                for space in spaces_before-subarea.spaces:
                                    space_areas[space].remove(subarea)
                                for space in subarea.spaces-spaces_before:
                                    space_areas[space].append(subarea)
                    break
                else:
                    raise ValueError

            # give altitudes to areas
            for space in level.spaces.all():
                for altitudemarker in space.altitudemarkers.all():
                    for area in space_areas[space.pk]:
                        if area.geometry.contains(altitudemarker.geometry):
                            area.altitude = altitudemarker.altitude
                            break
                    else:
                        raise ValueError(space.title)

            all_areas.extend(areas)
