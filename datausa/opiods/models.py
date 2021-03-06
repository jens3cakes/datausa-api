from datausa.database import db
from datausa.core.models import BaseModel
from datausa.attrs.consts import NATION, STATE, ALL
from datausa.attrs.models import Geo
from sqlalchemy.ext.declarative import declared_attr


class BaseOpiods(db.Model, BaseModel):
    __abstract__ = True
    __table_args__ = {"schema": "opiods"}
    supported_levels = {"year": [ALL]}
    source_title = 'Kaiser Family Foundation analysis of Centers for Disease Control and Prevention (CDC), National Center for Health Statistics'
    source_link = 'https://www.kff.org/other/state-indicator/opioid-overdose-death-rates/'
    source_org = 'Kaiser Family Foundation State Health Facts'

    @classmethod
    def get_supported_levels(cls):
        return {
            "year": [ALL],
            "geo": [ALL, NATION, STATE]
        }

    @classmethod
    def geo_filter(cls, level):
        if level == ALL:
            return True
        level_map = {STATE: "040", NATION: "010"}
        level_code = level_map[level]
        return cls.geo.startswith(level_code)

    @declared_attr
    def geo(cls):
        return db.Column(db.String(), db.ForeignKey(Geo.id), primary_key=True)


class DrugOverdoseDeathRate(BaseOpiods):
    __tablename__ = "drug_overdose_deathrate"
    median_moe = 1
    source_link = 'https://www.kff.org/other/state-indicator/opioid-overdose-death-rates/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D'
    year = db.Column(db.Integer(), primary_key=True)
    drug_overdose_ageadjusted = db.Column(db.String())


class OpiodOverdoseDeathRate(BaseOpiods):
    __tablename__ = "opioid_overdose_deathrate"
    median_moe = 1
    source_link = 'https://www.kff.org/other/state-indicator/opioid-overdose-death-rates/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D'
    year = db.Column(db.Integer(), primary_key=True)
    opioid_overdose_deathrate_ageadjusted = db.Column(db.String())


class NonMedUsePainMeds(BaseOpiods):
    __tablename__ = "non_medical_use_of_pain_releivers"
    median_moe = 1
    source_title = 'National Survey on Drug Use and Health'
    source_org = 'SAMHSA, Center for Behavioral Health Statistics and Quality'
    source_link = 'https://nsduhweb.rti.org/respweb/homepage.cfm'
    start_year = db.Column(db.Integer(), primary_key=True)
    year = db.Column(db.Integer(), primary_key=True)

    non_medical_use_of_pain_relievers = db.Column(db.String())
    non_medical_use_of_pain_relievers_lci = db.Column(db.String())
    non_medical_use_of_pain_relievers_uci = db.Column(db.String())

    @classmethod
    def get_supported_levels(cls):
        return {
            "year": [ALL],
            "start_year": [ALL],
            "geo": [ALL, NATION, STATE]
        }
