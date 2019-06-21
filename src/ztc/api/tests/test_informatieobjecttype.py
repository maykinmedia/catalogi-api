from unittest import skip

from django.urls import reverse
from rest_framework import status
from vng_api_common.tests import get_operation_url
from vng_api_common.constants import VertrouwelijkheidsAanduiding

from ...datamodel.tests.factories import (
    InformatieObjectTypeFactory, ZaakInformatieobjectTypeFactory,
    ZaakTypeFactory
)
from ...datamodel.models import InformatieObjectType
from .base import APITestCase


class InformatieObjectTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        """Retrieve a list of `InformatieObjectType` objects."""
        InformatieObjectTypeFactory.create()
        informatieobjecttype_list_url = get_operation_url('informatieobjecttype_list')

        response = self.client.get(informatieobjecttype_list_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `InformatieObjectType` object."""

        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=self.catalogus,
            zaaktypes=None,
            model=['http://www.example.com'],
            trefwoord=['abc', 'def'],
            datum_begin_geldigheid='2019-01-01',
        )
        informatieobjecttype_detail_url = get_operation_url(
            'informatieobjecttype_read',
            uuid=informatieobjecttype.uuid
        )

        response = self.client.get(informatieobjecttype_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            # 'categorie': 'informatieobjectcategorie',
            # 'einddatumObject': None,
            # 'ingangsdatumObject': '2018-01-01',
            # 'isVastleggingVoor': [],
            'catalogus': 'http://testserver{}'.format(self.catalogus_detail_url),
            # 'model': ['http://www.example.com'],
            'omschrijving': informatieobjecttype.omschrijving,
            # 'omschrijvingGeneriek': '',
            # 'toelichting': None,
            # 'trefwoord': ['abc', 'def'],
            'url': 'http://testserver{}'.format(informatieobjecttype_detail_url),
            'vertrouwelijkheidaanduiding': '',
            # 'isRelevantVoor': [],
            'beginGeldigheid': '2019-01-01',
            'eindeGeldigheid': None,
            'draft': True,
        }
        self.assertEqual(expected, response.json())

    @skip("Not MVP yet")
    def test_is_relevant_voor(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=self.catalogus,
            zaaktypes=None,
            model=['http://www.example.com'],
            trefwoord=['abc', 'def']
        )
        informatieobjecttype_detail_url = get_operation_url(
            'informatieobjecttype_read',
            catalogus_uuid=self.catalogus.uuid,
            uuid=informatieobjecttype.uuid
        )

        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)

        ziot = ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype,
            informatie_object_type=informatieobjecttype,
            volgnummer=1,
            richting='richting',
        )

        response = self.client.get(informatieobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('isRelevantVoor' in data)
        self.assertEqual(len(data['isRelevantVoor']), 1)
        self.assertEqual(
            data['isRelevantVoor'][0],
            'http://testserver{}'.format(reverse('zktiot-detail', args=[
                zaaktype.pk, ziot.pk
            ]))
        )

    @skip("Not MVP yet")
    def test_is_vastlegging_voor(self):
        pass

    def test_create_informatieobjecttype(self):
        data = {
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            'omschrijving': 'test',
            'vertrouwelijkheidaanduiding': VertrouwelijkheidsAanduiding.openbaar,
            'beginGeldigheid': '2019-01-01'
        }
        informatieobjecttype_list_url = get_operation_url('informatieobjecttype_list')

        response = self.client.post(informatieobjecttype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        informatieobjecttype = InformatieObjectType.objects.get()

        self.assertEqual(informatieobjecttype.omschrijving, 'test')
        self.assertEqual(informatieobjecttype.catalogus, self.catalogus)
        self.assertEqual(informatieobjecttype.draft, True)

    def test_publish_zaaktype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttypee_url = get_operation_url('informatieobjecttype_publish', uuid=informatieobjecttype.uuid)

        response = self.client.post(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        informatieobjecttype.refresh_from_db()

        self.assertEqual(informatieobjecttype.draft, False)

    def test_delete_zaaktype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttypee_url = get_operation_url('informatieobjecttype_read', uuid=informatieobjecttype.uuid)

        response = self.client.delete(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InformatieObjectType.objects.filter(id=informatieobjecttype.id))

    def test_delete_zaak_fail_not_draft(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(draft=False)
        informatieobjecttypee_url = get_operation_url('informatieobjecttype_read', uuid=informatieobjecttype.uuid)

        response = self.client.delete(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-draft object is forbidden')

