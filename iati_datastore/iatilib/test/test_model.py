from . import AppTestCase
from . import factories as fac

from iatilib.model import Activity, Resource, Stats
from iatilib import db


class TestResource(AppTestCase):
    def test_replace_activities(self):
        # Activites are not updated in place. We only receive entire
        # docs (resources) which contain many actitivites, so to update
        # the db we remove all activites relating to a resource (plus
        # dependant objects) and replace them. These tests are me
        # working out how to do that in sqlalchemy.

        res = fac.ResourceFactory.create(
            activities=[fac.ActivityFactory.build(
                iati_identifier=u"t1",
                title=u"t1"
            )]
        )
        Activity.query.filter_by(resource_url=res.url).delete()
        # at this point res.activities has not been cleared
        res.activities = [
            fac.ActivityFactory.create(
                iati_identifier=u"t1",
                title=u"t2",
            )
        ]
        db.session.commit()
        self.assertEquals(res.activities[0].title, u"t2")
        self.assertEquals(
            Resource.query.get(res.url).activities[0].title, u"t2")

    def test_replace_activity_w_many_dependant_rows(self):
        db.engine.echo = True
        res = fac.ResourceFactory.create(
            activities=[fac.ActivityFactory.build(
                participating_orgs=[
                    fac.ParticipationFactory.build()
                ],
                recipient_country_percentages=[
                    fac.CountryPercentageFactory.build()
                ],
                transactions=[
                    fac.TransactionFactory.build()
                ],
                sector_percentages=[
                    fac.SectorPercentageFactory.build()
                ],
                budgets=[
                    fac.BudgetFactory.build()
                ],
                websites=[
                    u"http://test.com"
                ]
            )]
        )
        Activity.query.filter_by(resource_url=res.url).delete()
        self.assertEquals(
            0,
            Activity.query.filter_by(resource_url=res.url).count()
        )

    def test_stats_counts(self):
        fac.ActivityFactory.create(
            iati_identifier="47045-ARM-202-G05-H-00",
            title="orig",
        )
        fac.ActivityFactory.create(
            iati_identifier="47045-ARM-202-G05-H-01",
            title="orig",
        )
        self.assertEquals(
            2, Activity.query.count()
        )
        self.assertEquals(
            2, Stats.query.filter_by(label='activities').first().count
        )
        db.session.query(Activity).delete()
        self.assertEquals(
            0, Activity.query.count()
        )
        self.assertEquals(
            0, Stats.query.filter_by(label='activities').first().count
        )
