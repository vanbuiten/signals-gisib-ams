from django.utils import timezone
from factory import Faker, SelfAttribute, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from signals_gisib.models import Signal
from signals_gisib.models.gisib import CollectionItem, EPRCurative
from signals_gisib.tests.fuzzy import FuzzyPoint
from signals_gisib.tests.utils import BBOX_AMSTERDAM


class CollectionItemFactory(DjangoModelFactory):
    class Meta:
        model = CollectionItem
        django_get_or_create = ('gisib_id', )

    gisib_id = Faker('random_int', min=1000, max=9999, step=1)
    object_kind_name = FuzzyChoice(['Boom', ])
    geometry = FuzzyPoint(*BBOX_AMSTERDAM)
    properties = {}
    raw_properties = {}


class SignalFactory(DjangoModelFactory):
    class Meta:
        model = Signal
        django_get_or_create = ('signal_id', )

    signal_id = Faker('random_int', min=1000, max=9999, step=1)
    signal_created_at = Faker('date_between', start_date=timezone.now() - timezone.timedelta(days=5),
                              end_date=timezone.now())
    signal_geometry = FuzzyPoint(*BBOX_AMSTERDAM)
    signal_extra_properties = {}


class EPRCurativeFactory(DjangoModelFactory):
    class Meta:
        model = EPRCurative
        django_get_or_create = ('gisib_id', )

    gisib_id = Faker('random_int', min=10000, max=19999, step=1)
    signal = SubFactory(SignalFactory)
    collection_item = SubFactory(CollectionItemFactory, gisib_id=SelfAttribute('..gisib_id'))
    original_request = {}
    original_response = {}
