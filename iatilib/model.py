from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,DateTime,Float,ForeignKey,UnicodeText,Boolean

from . import db


class IndexedResource(db.Model):
    __tablename__ = 'indexed_resource'
    id = Column(UnicodeText, primary_key=True)
    url = Column(UnicodeText)
    last_modified = Column(DateTime)
    state = Column(Integer)
    ckan_url = Column(UnicodeText)
    xml_blobs = relationship("RawXmlBlob",cascade="all")
    logerrors = relationship("LogError",cascade="all")


class RawXmlBlob(db.Model):
    __tablename__ = 'raw_xml_blob'
    parent_id = Column(UnicodeText, ForeignKey('indexed_resource.id'), nullable=False)
    id = Column(Integer, primary_key=True)
    raw_xml = Column(UnicodeText)
    parsed = Column(Boolean)
    activity = relationship(
        "Activity",
        cascade="all",
        uselist=False,
        backref="parent")
    parent = relationship('IndexedResource')


class LogError(db.Model):
    __tablename__ = 'logerror'
    id = Column(Integer, primary_key=True)
    parent_id = Column(UnicodeText, ForeignKey('indexed_resource.id'), nullable=False)
    level = Column(Integer)
    text = Column(UnicodeText)


class CodelistSector(db.Model):
    __tablename__ = 'codelist_sector'
    code = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    description = Column(UnicodeText)
    category = Column(Integer)
    category_name = Column(UnicodeText)
    category_description = Column(UnicodeText)


class Activity(db.Model):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    transaction = relationship("Transaction",cascade="all")
    sector = relationship("Sector",cascade="all")
    participatingorg = relationship("ParticipatingOrg",cascade="all")
    contactinfo = relationship("ContactInfo",cascade="all")
    date = relationship("ActivityDate",cascade="all")
    reportingorg = relationship("ReportingOrg",cascade="all")
    recipientcountry = relationship("RecipientCountry",cascade="all")
    recipientregion = relationship("RecipientRegion",cascade="all")
    collaborationtype = relationship("CollaborationType",cascade="all")
    defaultflowtype = relationship("DefaultFlowType",cascade="all")
    defaultaidtype = relationship("DefaultAidType",cascade="all")
    defaultfinancetype = relationship("DefaultFinanceType",cascade="all")
    iatiidentifier = relationship("IatiIdentifier",cascade="all")
    otheridentifier = relationship("OtherIdentifier",cascade="all")
    title = relationship("Title",cascade="all")
    description = relationship("Description",cascade="all")
    status = relationship("ActivityStatus",cascade="all")
    defaulttiedstatus = relationship("DefaultTiedStatus",cascade="all")
    policymarker = relationship("PolicyMarker",cascade="all")
    website = relationship("Website",cascade="all")
    location = relationship("Location",cascade="all")
    result = relationship("Result",cascade="all")
    conditions = relationship("Conditions",cascade="all")
    budget = relationship("Budget",cascade="all")
    planned_disbursement = relationship("PlannedDisbursement",cascade="all")
    related_activity = relationship("RelatedActivity",cascade="all")
    document_link = relationship("DocumentLink",cascade="all")
    legacy_data = relationship("LegacyData",cascade="all")
    parent_id = Column(Integer, ForeignKey('raw_xml_blob.id'), nullable=False)
    version = Column(Float)	# @version
    last_updated_datetime = Column(DateTime)	# @last-updated-datetime
    lang = Column(UnicodeText)	# @xml:lang
    default_currency = Column(UnicodeText)	# @default-currency
    hierarchy = Column(Float)	# @hierarchy
    linked_data_uri = Column(UnicodeText)	# @linked-data-uri
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['version'] = _nav(logger, xml, [], attrib='version', parser=_parse_float)
        data['last_updated_datetime'] = _nav(logger, xml, [], attrib='last-updated-datetime', parser=_parse_datetime)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        data['default_currency'] = _nav(logger, xml, [], attrib='default-currency')
        data['hierarchy'] = _nav(logger, xml, [], attrib='hierarchy', parser=_parse_float)
        data['linked_data_uri'] = _nav(logger, xml, [], attrib='linked-data-uri')
        out = Activity(**data)
        for child_xml in xml.findall('transaction'):
            out.transaction.append( Transaction._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('sector'):
            out.sector.append( Sector._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('participating-org'):
            out.participatingorg.append( ParticipatingOrg._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('contact-info'):
            out.contactinfo.append( ContactInfo._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('activity-date'):
            out.date.append( ActivityDate._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('reporting-org'):
            out.reportingorg.append( ReportingOrg._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('recipient-country'):
            out.recipientcountry.append( RecipientCountry._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('recipient-region'):
            out.recipientregion.append( RecipientRegion._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('collaboration-type'):
            out.collaborationtype.append( CollaborationType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('default-flow-type'):
            out.defaultflowtype.append( DefaultFlowType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('default-aid-type'):
            out.defaultaidtype.append( DefaultAidType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('default-finance-type'):
            out.defaultfinancetype.append( DefaultFinanceType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('iati-identifier'):
            out.iatiidentifier.append( IatiIdentifier._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('other-identifier'):
            out.otheridentifier.append( OtherIdentifier._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('title'):
            out.title.append( Title._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('description'):
            out.description.append( Description._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('activity-status'):
            out.status.append( ActivityStatus._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('default-tied-status'):
            out.defaulttiedstatus.append( DefaultTiedStatus._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('policy-marker'):
            out.policymarker.append( PolicyMarker._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('activity-website'):
            out.website.append( Website._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('location'):
            out.location.append( Location._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('result'):
            out.result.append( Result._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('conditions'):
            out.conditions.append( Conditions._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('budget'):
            out.budget.append( Budget._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('planned-disbursement'):
            out.planned_disbursement.append( PlannedDisbursement._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('related-activity'):
            out.related_activity.append( RelatedActivity._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('document-link'):
            out.document_link.append( DocumentLink._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('legacy-data'):
            out.legacy_data.append( LegacyData._parse_xml(logger,child_xml) )
        return out

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    value = relationship("TransactionValue", cascade="all", uselist=False)
    description = relationship("TransactionDescription",cascade="all")
    type = relationship("TransactionType", cascade="all", uselist=False)
    provider_org = relationship("TransactionProviderOrg",cascade="all")
    receiver_org = relationship("TransactionReceiverOrg",cascade="all")
    date = relationship("TransactionDate",cascade="all")
    flow_type = relationship("TransactionFlowType",cascade="all")
    aid_type = relationship("TransactionAidType",cascade="all")
    finance_type = relationship("TransactionFinanceType",cascade="all")
    tied_status = relationship("TransactionTiedStatus",cascade="all")
    disbursement_channel = relationship("TransactionDisbursementChannel",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    ref = Column(UnicodeText)	# @ref
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['ref'] = _nav(logger, xml, [], attrib='ref')
        out = Transaction(**data)
        for child_xml in xml.findall('value'):
            out.value = TransactionValue._parse_xml(logger,child_xml)
        for child_xml in xml.findall('description'):
            out.description.append( TransactionDescription._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('transaction-type'):
            out.type = TransactionType._parse_xml(logger,child_xml)
        for child_xml in xml.findall('provider-org'):
            out.provider_org.append( TransactionProviderOrg._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('receiver-org'):
            out.receiver_org.append( TransactionReceiverOrg._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('transaction-date'):
            out.date.append( TransactionDate._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('flow-type'):
            out.flow_type.append( TransactionFlowType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('aid-type'):
            out.aid_type.append( TransactionAidType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('finance-type'):
            out.finance_type.append( TransactionFinanceType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('tied-status'):
            out.tied_status.append( TransactionTiedStatus._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('disbursement-channel'):
            out.disbursement_channel.append( TransactionDisbursementChannel._parse_xml(logger,child_xml) )
        return out

class TransactionValue(db.Model):
    __tablename__ = 'transaction_value'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(Float)	# text()
    currency = Column(UnicodeText)	# @currency
    value_date = Column(DateTime)	# @value-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True, parser=_parse_float)
        data['currency'] = _nav(logger, xml, [], attrib='currency')
        data['value_date'] = _nav(logger, xml, [], attrib='value-date', parser=_parse_datetime)
        out = TransactionValue(**data)
        return out

class TransactionDescription(db.Model):
    __tablename__ = 'transaction_description'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = TransactionDescription(**data)
        return out

class TransactionType(db.Model):
    __tablename__ = 'transaction_type'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = TransactionType(**data)
        return out

class TransactionProviderOrg(db.Model):
    __tablename__ = 'transaction_provider_org'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    ref = Column(UnicodeText)	# @ref
    provider_activity_id = Column(UnicodeText)	# @provider-activity-id
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['ref'] = _nav(logger, xml, [], attrib='ref')
        data['provider_activity_id'] = _nav(logger, xml, [], attrib='provider-activity-id')
        out = TransactionProviderOrg(**data)
        return out

class TransactionReceiverOrg(db.Model):
    __tablename__ = 'transaction_receiver_org'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    ref = Column(UnicodeText)	# @ref
    receiver_activity_id = Column(UnicodeText)	# @receiver-activity-id
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['ref'] = _nav(logger, xml, [], attrib='ref')
        data['receiver_activity_id'] = _nav(logger, xml, [], attrib='receiver-activity-id')
        out = TransactionReceiverOrg(**data)
        return out

class TransactionDate(db.Model):
    __tablename__ = 'transaction_date'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    iso_date = Column(DateTime)	# @iso-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        out = TransactionDate(**data)
        return out

class TransactionFlowType(db.Model):
    __tablename__ = 'transaction_flow_type'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = TransactionFlowType(**data)
        return out

class TransactionAidType(db.Model):
    __tablename__ = 'transaction_aid_type'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = TransactionAidType(**data)
        return out

class TransactionFinanceType(db.Model):
    __tablename__ = 'transaction_finance_type'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = TransactionFinanceType(**data)
        return out

class TransactionTiedStatus(db.Model):
    __tablename__ = 'transaction_tied_status'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = TransactionTiedStatus(**data)
        return out

class TransactionDisbursementChannel(db.Model):
    __tablename__ = 'transaction_disbursement_channel'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = TransactionDisbursementChannel(**data)
        return out

class Sector(db.Model):
    __tablename__ = 'sector'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(Integer)	# @code
    vocabulary = Column(UnicodeText)	# @vocabulary
    percentage = Column(Float)	# @percentage
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code', parser=_parse_int)
        data['vocabulary'] = _nav(logger, xml, [], attrib='vocabulary')
        data['percentage'] = _nav(logger, xml, [], attrib='percentage', parser=_parse_float)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = Sector(**data)
        return out

class ActivityDate(db.Model):
    __tablename__ = 'activity_date'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    type = Column(UnicodeText)	# @type
    iso_date = Column(DateTime)	# @iso-date
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ActivityDate(**data)
        return out

class ContactInfo(db.Model):
    __tablename__ = 'contactinfo'
    id = Column(Integer, primary_key=True)
    organisation = relationship("ContactInfoOrganisation",cascade="all")
    person = relationship("ContactInfoPerson",cascade="all")
    telephone = relationship("ContactInfoTelephone",cascade="all")
    email = relationship("ContactInfoEmail",cascade="all")
    mail = relationship("ContactInfoMail",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        out = ContactInfo(**data)
        for child_xml in xml.findall('organisation'):
            out.organisation.append( ContactInfoOrganisation._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('person-name'):
            out.person.append( ContactInfoPerson._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('telephone'):
            out.telephone.append( ContactInfoTelephone._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('email'):
            out.email.append( ContactInfoEmail._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('mailing-address'):
            out.mail.append( ContactInfoMail._parse_xml(logger,child_xml) )
        return out

class ContactInfoOrganisation(db.Model):
    __tablename__ = 'contactinfo_organisation'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('contactinfo.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        out = ContactInfoOrganisation(**data)
        return out

class ContactInfoPerson(db.Model):
    __tablename__ = 'contactinfo_person'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('contactinfo.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        out = ContactInfoPerson(**data)
        return out

class ContactInfoTelephone(db.Model):
    __tablename__ = 'contactinfo_telephone'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('contactinfo.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        out = ContactInfoTelephone(**data)
        return out

class ContactInfoEmail(db.Model):
    __tablename__ = 'contactinfo_email'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('contactinfo.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        out = ContactInfoEmail(**data)
        return out

class ContactInfoMail(db.Model):
    __tablename__ = 'contactinfo_mail'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('contactinfo.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        out = ContactInfoMail(**data)
        return out

class ParticipatingOrg(db.Model):
    __tablename__ = 'participatingorg'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    ref = Column(UnicodeText)	# @ref
    type = Column(UnicodeText)	# @type
    role = Column(UnicodeText)	# @role
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['ref'] = _nav(logger, xml, [], attrib='ref')
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['role'] = _nav(logger, xml, [], attrib='role')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ParticipatingOrg(**data)
        return out

class ReportingOrg(db.Model):
    __tablename__ = 'reportingorg'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    ref = Column(UnicodeText)	# @ref
    type = Column(UnicodeText)	# @type
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['ref'] = _nav(logger, xml, [], attrib='ref')
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ReportingOrg(**data)
        return out

class RecipientCountry(db.Model):
    __tablename__ = 'recipientcountry'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    percentage = Column(Float)	# @percentage
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['percentage'] = _nav(logger, xml, [], attrib='percentage', parser=_parse_float)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = RecipientCountry(**data)
        return out

class RecipientRegion(db.Model):
    __tablename__ = 'recipientregion'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    percentage = Column(Float)	# @percentage
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['percentage'] = _nav(logger, xml, [], attrib='percentage', parser=_parse_float)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = RecipientRegion(**data)
        return out

class CollaborationType(db.Model):
    __tablename__ = 'collaborationtype'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = CollaborationType(**data)
        return out

class DefaultFlowType(db.Model):
    __tablename__ = 'defaultflowtype'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = DefaultFlowType(**data)
        return out

class DefaultAidType(db.Model):
    __tablename__ = 'defaultaidtype'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = DefaultAidType(**data)
        return out

class DefaultFinanceType(db.Model):
    __tablename__ = 'defaultfinancetype'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = DefaultFinanceType(**data)
        return out

class IatiIdentifier(db.Model):
    __tablename__ = 'iatiidentifier'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        out = IatiIdentifier(**data)
        return out

class OtherIdentifier(db.Model):
    __tablename__ = 'otheridentifier'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    owner_ref = Column(UnicodeText)	# @owner-ref
    owner_name = Column(UnicodeText)	# @owner-name
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['owner_ref'] = _nav(logger, xml, [], attrib='owner-ref')
        data['owner_name'] = _nav(logger, xml, [], attrib='owner-name')
        out = OtherIdentifier(**data)
        return out

class Title(db.Model):
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = Title(**data)
        return out

class Description(db.Model):
    __tablename__ = 'description'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    type = Column(UnicodeText)	# @type
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = Description(**data)
        return out

class ActivityStatus(db.Model):
    __tablename__ = 'activity_status'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ActivityStatus(**data)
        return out

class DefaultTiedStatus(db.Model):
    __tablename__ = 'defaulttiedstatus'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = DefaultTiedStatus(**data)
        return out

class PolicyMarker(db.Model):
    __tablename__ = 'policymarker'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    vocabulary = Column(UnicodeText)	# @vocabulary
    significance = Column(UnicodeText)	# @significance
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['vocabulary'] = _nav(logger, xml, [], attrib='vocabulary')
        data['significance'] = _nav(logger, xml, [], attrib='significance')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = PolicyMarker(**data)
        return out

class Website(db.Model):
    __tablename__ = 'activity_website'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        out = Website(**data)
        return out

class Location(db.Model):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    type = relationship("LocationType",cascade="all")
    name = relationship("LocationName",cascade="all")
    description = relationship("LocationDescription",cascade="all")
    administrative = relationship("LocationAdministrative",cascade="all")
    coordinates = relationship("LocationCoordinates",cascade="all")
    gazetteerentry = relationship("LocationGazetteerEntry",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    percentage = Column(Float)	# @percentage
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['percentage'] = _nav(logger, xml, [], attrib='percentage', parser=_parse_float)
        out = Location(**data)
        for child_xml in xml.findall('location-type'):
            out.type.append( LocationType._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('name'):
            out.name.append( LocationName._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('description'):
            out.description.append( LocationDescription._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('administrative'):
            out.administrative.append( LocationAdministrative._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('coordinates'):
            out.coordinates.append( LocationCoordinates._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('gazetteer-entry'):
            out.gazetteerentry.append( LocationGazetteerEntry._parse_xml(logger,child_xml) )
        return out

class Result(db.Model):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    title = relationship("ResultTitle",cascade="all")
    description = relationship("ResultDescription",cascade="all")
    indicator = relationship("ResultIndicator",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    type = Column(UnicodeText)	# @type
    aggregation_status = Column(Boolean)	# @aggregation-status
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['aggregation_status'] = _nav(logger, xml, [], attrib='aggregation-status', parser=_parse_boolean)
        out = Result(**data)
        for child_xml in xml.findall('title'):
            out.title.append( ResultTitle._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('description'):
            out.description.append( ResultDescription._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('indicator'):
            out.indicator.append( ResultIndicator._parse_xml(logger,child_xml) )
        return out

class Conditions(db.Model):
    __tablename__ = 'conditions'
    id = Column(Integer, primary_key=True)
    condition = relationship("Condition",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    attached = Column(Boolean)	# @attached
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['attached'] = _nav(logger, xml, [], attrib='attached', parser=_parse_boolean)
        out = Conditions(**data)
        for child_xml in xml.findall('condition'):
            out.condition.append( Condition._parse_xml(logger,child_xml) )
        return out

class Budget(db.Model):
    __tablename__ = 'budget'
    id = Column(Integer, primary_key=True)
    period_start = relationship("BudgetPeriodStart",cascade="all")
    period_end = relationship("BudgetPeriodEnd",cascade="all")
    value = relationship("BudgetValue",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    type = Column(UnicodeText)	# @type
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['type'] = _nav(logger, xml, [], attrib='type')
        out = Budget(**data)
        for child_xml in xml.findall('period-start'):
            out.period_start.append( BudgetPeriodStart._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('period-end'):
            out.period_end.append( BudgetPeriodEnd._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('value'):
            out.value.append( BudgetValue._parse_xml(logger,child_xml) )
        return out

class PlannedDisbursement(db.Model):
    __tablename__ = 'planned_disbursement'
    id = Column(Integer, primary_key=True)
    period_start = relationship("PlannedDisbursementPeriodStart",cascade="all")
    period_end = relationship("PlannedDisbursementPeriodEnd",cascade="all")
    value = relationship("PlannedDisbursementValue",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    updated = Column(UnicodeText)	# @updated
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['updated'] = _nav(logger, xml, [], attrib='updated')
        out = PlannedDisbursement(**data)
        for child_xml in xml.findall('period-start'):
            out.period_start.append( PlannedDisbursementPeriodStart._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('period-end'):
            out.period_end.append( PlannedDisbursementPeriodEnd._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('value'):
            out.value.append( PlannedDisbursementValue._parse_xml(logger,child_xml) )
        return out

class RelatedActivity(db.Model):
    __tablename__ = 'related_activity'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    ref = Column(UnicodeText)	# @ref
    type = Column(UnicodeText)	# @type
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['ref'] = _nav(logger, xml, [], attrib='ref')
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = RelatedActivity(**data)
        return out

class DocumentLink(db.Model):
    __tablename__ = 'document_link'
    id = Column(Integer, primary_key=True)
    title = relationship("DocumentLinkTitle",cascade="all")
    category = relationship("DocumentLinkCategory",cascade="all")
    language = relationship("DocumentLinkLanguage",cascade="all")
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    url = Column(UnicodeText)	# @url
    format = Column(UnicodeText)	# @format
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['url'] = _nav(logger, xml, [], attrib='url')
        data['format'] = _nav(logger, xml, [], attrib='format')
        out = DocumentLink(**data)
        for child_xml in xml.findall('title'):
            out.title.append( DocumentLinkTitle._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('category'):
            out.category.append( DocumentLinkCategory._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('language'):
            out.language.append( DocumentLinkLanguage._parse_xml(logger,child_xml) )
        return out

class LegacyData(db.Model):
    __tablename__ = 'legacy_data'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    name = Column(UnicodeText)	# @name
    value = Column(UnicodeText)	# @value
    iati_equivalent = Column(UnicodeText)	# @iati-equivalent
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['name'] = _nav(logger, xml, [], attrib='name')
        data['value'] = _nav(logger, xml, [], attrib='value')
        data['iati_equivalent'] = _nav(logger, xml, [], attrib='iati-equivalent')
        out = LegacyData(**data)
        return out

class LocationType(db.Model):
    __tablename__ = 'location_type'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = LocationType(**data)
        return out

class LocationName(db.Model):
    __tablename__ = 'location_name'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = LocationName(**data)
        return out

class LocationDescription(db.Model):
    __tablename__ = 'location_description'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = LocationDescription(**data)
        return out

class LocationAdministrative(db.Model):
    __tablename__ = 'location_administrative'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    country = Column(UnicodeText)	# @country
    adm1 = Column(UnicodeText)	# @adm1
    adm2 = Column(UnicodeText)	# @adm2
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['country'] = _nav(logger, xml, [], attrib='country')
        data['adm1'] = _nav(logger, xml, [], attrib='adm1')
        data['adm2'] = _nav(logger, xml, [], attrib='adm2')
        out = LocationAdministrative(**data)
        return out

class LocationCoordinates(db.Model):
    __tablename__ = 'location_coordinates'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    latitude = Column(Float)	# @latitude
    longitude = Column(Float)	# @longitude
    precision = Column(UnicodeText)	# @precision
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['latitude'] = _nav(logger, xml, [], attrib='latitude', parser=_parse_float)
        data['longitude'] = _nav(logger, xml, [], attrib='longitude', parser=_parse_float)
        data['precision'] = _nav(logger, xml, [], attrib='precision')
        out = LocationCoordinates(**data)
        return out

class LocationGazetteerEntry(db.Model):
    __tablename__ = 'location_gazetteerentry'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    gazetteer_ref = Column(UnicodeText)	# @gazetteer-ref
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['gazetteer_ref'] = _nav(logger, xml, [], attrib='gazetteer-ref')
        out = LocationGazetteerEntry(**data)
        return out

class ResultTitle(db.Model):
    __tablename__ = 'result_title'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ResultTitle(**data)
        return out

class ResultDescription(db.Model):
    __tablename__ = 'result_description'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    type = Column(UnicodeText)	# @type
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ResultDescription(**data)
        return out

class ResultIndicator(db.Model):
    __tablename__ = 'result_indicator'
    id = Column(Integer, primary_key=True)
    title = relationship("ResultIndicatorTitle",cascade="all")
    description = relationship("ResultIndicatorDescription",cascade="all")
    baseline = relationship("ResultIndicatorBaseline",cascade="all")
    period = relationship("ResultIndicatorPeriod",cascade="all")
    parent_id = Column(Integer, ForeignKey('result.id'), nullable=False)
    measure = Column(UnicodeText)	# @measure
    ascending = Column(Boolean)	# @ascending
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['measure'] = _nav(logger, xml, [], attrib='measure')
        data['ascending'] = _nav(logger, xml, [], attrib='ascending', parser=_parse_boolean)
        out = ResultIndicator(**data)
        for child_xml in xml.findall('title'):
            out.title.append( ResultIndicatorTitle._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('description'):
            out.description.append( ResultIndicatorDescription._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('baseline'):
            out.baseline.append( ResultIndicatorBaseline._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('period'):
            out.period.append( ResultIndicatorPeriod._parse_xml(logger,child_xml) )
        return out

class ResultIndicatorTitle(db.Model):
    __tablename__ = 'result_indicator_title'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result_indicator.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ResultIndicatorTitle(**data)
        return out

class ResultIndicatorDescription(db.Model):
    __tablename__ = 'result_indicator_description'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result_indicator.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    type = Column(UnicodeText)	# @type
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['type'] = _nav(logger, xml, [], attrib='type')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ResultIndicatorDescription(**data)
        return out

class ResultIndicatorBaseline(db.Model):
    __tablename__ = 'result_indicator_baseline'
    id = Column(Integer, primary_key=True)
    comment = relationship("ResultIndicatorBaselineComment",cascade="all")
    parent_id = Column(Integer, ForeignKey('result_indicator.id'), nullable=False)
    year = Column(Float)	# @year
    value = Column(UnicodeText)	# @value
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['year'] = _nav(logger, xml, [], attrib='year', parser=_parse_float)
        data['value'] = _nav(logger, xml, [], attrib='value')
        out = ResultIndicatorBaseline(**data)
        for child_xml in xml.findall('comment'):
            out.comment.append( ResultIndicatorBaselineComment._parse_xml(logger,child_xml) )
        return out

class ResultIndicatorPeriod(db.Model):
    __tablename__ = 'result_indicator_period'
    id = Column(Integer, primary_key=True)
    start = relationship("ResultIndicatorPeriodStart",cascade="all")
    end = relationship("ResultIndicatorPeriodEnd",cascade="all")
    target = relationship("ResultIndicatorPeriodTarget",cascade="all")
    actual = relationship("ResultIndicatorPeriodActual",cascade="all")
    parent_id = Column(Integer, ForeignKey('result_indicator.id'), nullable=False)
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        out = ResultIndicatorPeriod(**data)
        for child_xml in xml.findall('period-start'):
            out.start.append( ResultIndicatorPeriodStart._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('period-end'):
            out.end.append( ResultIndicatorPeriodEnd._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('target'):
            out.target.append( ResultIndicatorPeriodTarget._parse_xml(logger,child_xml) )
        for child_xml in xml.findall('actual'):
            out.actual.append( ResultIndicatorPeriodActual._parse_xml(logger,child_xml) )
        return out

class ResultIndicatorBaselineComment(db.Model):
    __tablename__ = 'result_indicator_baseline_comment'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result_indicator_baseline.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ResultIndicatorBaselineComment(**data)
        return out

class ResultIndicatorPeriodStart(db.Model):
    __tablename__ = 'result_indicator_period_start'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result_indicator_period.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    iso_date = Column(DateTime)	# @iso-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        out = ResultIndicatorPeriodStart(**data)
        return out

class ResultIndicatorPeriodEnd(db.Model):
    __tablename__ = 'result_indicator_period_end'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result_indicator_period.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    iso_date = Column(DateTime)	# @iso-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        out = ResultIndicatorPeriodEnd(**data)
        return out

class ResultIndicatorPeriodTarget(db.Model):
    __tablename__ = 'result_indicator_period_target'
    id = Column(Integer, primary_key=True)
    comment = relationship("ResultIndicatorPeriodTargetComment",cascade="all")
    parent_id = Column(Integer, ForeignKey('result_indicator_period.id'), nullable=False)
    value = Column(UnicodeText)	# @value
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['value'] = _nav(logger, xml, [], attrib='value')
        out = ResultIndicatorPeriodTarget(**data)
        for child_xml in xml.findall('comment'):
            out.comment.append( ResultIndicatorPeriodTargetComment._parse_xml(logger,child_xml) )
        return out

class ResultIndicatorPeriodActual(db.Model):
    __tablename__ = 'result_indicator_period_actual'
    id = Column(Integer, primary_key=True)
    comment = relationship("ResultIndicatorPeriodActualComment",cascade="all")
    parent_id = Column(Integer, ForeignKey('result_indicator_period.id'), nullable=False)
    value = Column(UnicodeText)	# @value
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['value'] = _nav(logger, xml, [], attrib='value')
        out = ResultIndicatorPeriodActual(**data)
        for child_xml in xml.findall('comment'):
            out.comment.append( ResultIndicatorPeriodActualComment._parse_xml(logger,child_xml) )
        return out

class ResultIndicatorPeriodTargetComment(db.Model):
    __tablename__ = 'result_indicator_period_target_comment'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result_indicator_period_target.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ResultIndicatorPeriodTargetComment(**data)
        return out

class ResultIndicatorPeriodActualComment(db.Model):
    __tablename__ = 'result_indicator_period_actual_comment'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('result_indicator_period_actual.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = ResultIndicatorPeriodActualComment(**data)
        return out

class Condition(db.Model):
    __tablename__ = 'condition'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('conditions.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    type = Column(UnicodeText)	# @type
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['type'] = _nav(logger, xml, [], attrib='type')
        out = Condition(**data)
        return out

class BudgetPeriodStart(db.Model):
    __tablename__ = 'budget_period_start'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('budget.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    iso_date = Column(DateTime)	# @iso-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        out = BudgetPeriodStart(**data)
        return out

class BudgetPeriodEnd(db.Model):
    __tablename__ = 'budget_period_end'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('budget.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    iso_date = Column(DateTime)	# @iso-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        out = BudgetPeriodEnd(**data)
        return out

class BudgetValue(db.Model):
    __tablename__ = 'budget_value'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('budget.id'), nullable=False)
    text = Column(Float)	# text()
    currency = Column(UnicodeText)	# @currency
    value_date = Column(DateTime)	# @value-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True, parser=_parse_float)
        data['currency'] = _nav(logger, xml, [], attrib='currency')
        data['value_date'] = _nav(logger, xml, [], attrib='value-date', parser=_parse_datetime)
        out = BudgetValue(**data)
        return out

class PlannedDisbursementPeriodStart(db.Model):
    __tablename__ = 'planned_disbursement_period_start'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('planned_disbursement.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    iso_date = Column(DateTime)	# @iso-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        out = PlannedDisbursementPeriodStart(**data)
        return out

class PlannedDisbursementPeriodEnd(db.Model):
    __tablename__ = 'planned_disbursement_period_end'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('planned_disbursement.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    iso_date = Column(DateTime)	# @iso-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['iso_date'] = _nav(logger, xml, [], attrib='iso-date', parser=_parse_datetime)
        out = PlannedDisbursementPeriodEnd(**data)
        return out

class PlannedDisbursementValue(db.Model):
    __tablename__ = 'planned_disbursement_value'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('planned_disbursement.id'), nullable=False)
    text = Column(Float)	# text()
    currency = Column(UnicodeText)	# @currency
    value_date = Column(DateTime)	# @value-date
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True, parser=_parse_float)
        data['currency'] = _nav(logger, xml, [], attrib='currency')
        data['value_date'] = _nav(logger, xml, [], attrib='value-date', parser=_parse_datetime)
        out = PlannedDisbursementValue(**data)
        return out

class DocumentLinkTitle(db.Model):
    __tablename__ = 'document_link_title'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('document_link.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = DocumentLinkTitle(**data)
        return out

class DocumentLinkCategory(db.Model):
    __tablename__ = 'document_link_category'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('document_link.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = DocumentLinkCategory(**data)
        return out

class DocumentLinkLanguage(db.Model):
    __tablename__ = 'document_link_language'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('document_link.id'), nullable=False)
    text = Column(UnicodeText)	# text()
    code = Column(UnicodeText)	# @code
    lang = Column(UnicodeText)	# @xml:lang
    @classmethod
    def _parse_xml(cls,logger,xml):
        from parser import _nav, _parse_float, _parse_int, _parse_datetime, _parse_boolean
        data = {}
        data['text'] = _nav(logger, xml, [], text=True)
        data['code'] = _nav(logger, xml, [], attrib='code')
        data['lang'] = _nav(logger, xml, [], attrib='xml:lang')
        out = DocumentLinkLanguage(**data)
        return out
