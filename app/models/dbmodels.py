from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, SmallInteger, TIMESTAMP, Date, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from config.configdb import db
from sqlalchemy_serializer import SerializerMixin


class Campaign(db.Model, SerializerMixin):
    __tablename__ = 'campaigns'

    campaign_id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50), nullable=False)
    status = Column(db.SmallInteger(), nullable=False, default=0)
    begin_date = Column(db.TIMESTAMP(), nullable=False, default=datetime.now())
    end_date = Column(db.TIMESTAMP(), nullable=True)
    creation_date = Column(db.TIMESTAMP(), nullable=False, default=datetime.now())
    rule_id = Column(db.Integer, ForeignKey('campaign_rules.rule_id'), nullable=True)
    poi_campaign = Column(db.Boolean(), nullable=True)


class CampaignRule(db.Model, SerializerMixin):
    __tablename__ = 'campaign_rules'

    rule_id = Column(db.Integer, primary_key=True)
    age_start = Column(db.Date, nullable=True)
    age_end = Column(db.Date, nullable=True)
    gender = Column(db.SmallInteger, nullable=True)
    oncar = Column(db.Boolean, nullable=True)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    user_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), nullable=False)
    email = Column(db.String(50), nullable=False)
    google_id = Column(db.String, unique=True, nullable=True)
    phone = Column(db.String(14), nullable=True)
    address = Column(db.String(60), nullable=True)
    birthday = Column(db.Date, nullable=False)
    gender = Column(db.SmallInteger, nullable=True)
    oncar = Column(db.Boolean, nullable=True)

class NotificationTouchpoint(db.Model, SerializerMixin):
    __tablename__ = 'notification_touchpoints'

    touchpoint_id = Column(db.Integer, primary_key=True)
    channel = Column(db.Integer, nullable=False)
    topic = Column(db.String(60), nullable=True)

class CampaignNotification(db.Model, SerializerMixin):
    __tablename__ = 'campaign_notifications'

    notification_id = Column(db.Integer, primary_key=True)
    campaign_id = Column(db.Integer, ForeignKey('campaigns.campaign_id'))
    notification_title = Column(db.String(40), nullable=False)
    message_template = Column(db.String, nullable=False)
    priority = Column(db.SmallInteger, nullable=False, default=0)
    responsive = Column(db.Boolean, nullable=False, default=False)
    touchpoint_id = Column(db.Integer, ForeignKey('notification_touchpoints.touchpoint_id'), nullable=False)
    notification_type = Column(db.String(30), nullable=True)
    notification_icon_type = Column(db.String(40), nullable=True)
    poi_notification = Column(db.Boolean, nullable=True)

    pois = relationship('PointOfInterest', secondary='notification_pois', back_populates='notifications')

class PointOfInterest(db.Model, SerializerMixin):
    __tablename__ = 'points_of_interest'

    poi_id = Column(db.Integer, primary_key=True)
    poi_type = Column(db.String, nullable=False)
    poi_name = Column(db.String(40), nullable=False)
    poi_description = Column(db.String, nullable=True)
    latitude = Column(db.Float, nullable=False)
    longitude = Column(db.Float, nullable=False)

    notifications = relationship('CampaignNotification', secondary='notification_pois', back_populates='pois')

class NotificationPois(db.Model, SerializerMixin):
    __tablename__ = 'notification_pois'

    notification_id = Column(db.Integer, ForeignKey('campaign_notifications.notification_id'), primary_key=True)
    poi_id = Column(db.Integer, ForeignKey('points_of_interest.poi_id'), primary_key=True)


    __table_args__= (
        PrimaryKeyConstraint(notification_id, poi_id),
        {},
    )