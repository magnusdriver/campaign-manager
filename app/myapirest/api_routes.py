from flask import Flask, request, jsonify
from models.dbmodels import Campaign, User, CampaignNotification, NotificationTouchpoint, PointOfInterest
from datetime import datetime
from config.configdb import dbUrl, db
import yaml, json

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = dbUrl

db.init_app(app)

@app.route("/users", methods = ["GET", "POST"])
def get_post_users():
    match request.method:
        case "GET":
            try:
                users = db.session.query(User).order_by(User.name).all()
                serializedList = [user.to_dict() for user in users]
                return jsonify(serializedList)

            except Exception as e:
                return jsonify({'error': str(e)}), 500
        case "POST":
            try:
                userData = request.get_json()
                newUser = User(
                    name=userData["name"],
                    email=userData["email"],
                    phone=userData["phone"],
                    birthday=userData["birthday"],
                    gender=userData["gender"]
                )

                db.session.add(newUser)
                db.session.commit()
                db.session.flush()

                return jsonify({'message': f'Nuevo usuario con id {newUser.user_id} creado.'})

            except Exception as e:
                return jsonify({'error': str(e)}), 500
            

    
@app.get("/campaigns")    
def list_campaigns():
    try:

        query = db.session.query(Campaign).order_by(Campaign.campaign_id).all()

        serializedList = [row.to_dict() for row in query]

        return jsonify(serializedList)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.post("/campaigns")
def create_campaign():
    try:
        campaignData = request.get_json()

        print(campaignData)

        args = {
            "title": campaignData.get("title"),
            "status": campaignData.get("status"),
            "begin_date": campaignData.get("begin_date"),
            "end_date": campaignData.get("end_date"),
            "creation_date": campaignData.get("creation_date"),
            "rule_id": campaignData.get("rule_id"),
            "poi_campaign": campaignData.get("poi_campaign")
        }

        newCampaign = Campaign(**args)

        print(newCampaign.title)
        db.session.add(newCampaign)
        db.session.commit()
        db.session.flush()

        return jsonify({'message': f'Nueva campaña con id {newCampaign.campaign_id} creada.'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route("/campaigns/<int:id>", methods=["GET", "POST", "DELETE"])
def get_campaigns(id):
    campaign = db.get_or_404(Campaign, id)

    match request.method:
        case "DELETE":
            try:
                db.session.delete(campaign)
                db.session.commit()

                return jsonify({'message': f'Se eliminó la campaña'})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            
@app.route("/campaigns/<int:id>/notifications", methods=["GET", "POST", "DELETE"])
def campaigns_notifications(id):
    match request.method:
        case "POST":
            try:
                campaignNotificationData = request.get_json()

                print(campaignNotificationData)

                args = {
                    "campaign_id": id,
                    "notification_title": campaignNotificationData.get("notification_title"),
                    "message_template": campaignNotificationData.get("message_template"),
                    "priority": campaignNotificationData.get("priority"),
                    "responsive": campaignNotificationData.get("responsive"),
                    "touchpoint_id": campaignNotificationData.get("touchpoint_id"),
                    "notification_type": campaignNotificationData.get("notification_type"),
                    "notification_icon_type": campaignNotificationData.get("notification_icon_type"),
                    "poi_notification": campaignNotificationData.get("poi_notification")
                }

                newCampaignNotification = CampaignNotification(**args)
                print(newCampaignNotification.message_template)
                print(newCampaignNotification.responsive)

                if "poi_type" in campaignNotificationData:
                    poisByType = db.session.query(PointOfInterest).filter(PointOfInterest.poi_type == campaignNotificationData["poi_type"]).all()
                    newCampaignNotification.pois.extend(poisByType)

                db.session.add(newCampaignNotification)
                db.session.commit()
                db.session.flush()

                return jsonify({'message': f'Nueva notificación con id {newCampaignNotification.notification_id} creada.'})
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500

@app.route("/campaign-notifications", methods=["GET", "POST"])
def get_campaigns_notifications():
    match request.method:
        case "POST":
            try:
                campaignNotificationData = request.get_json()

                print(campaignNotificationData)

                newCampaignNotification = CampaignNotification(
                    campaign_id=campaignNotificationData["campaign_id"],
                    notification_title=campaignNotificationData["notification_title"],
                    message_template=campaignNotificationData["message_template"],
                    priority=campaignNotificationData["priority"] if "priority" in campaignNotificationData else None,
                    responsive=campaignNotificationData["responsive"] if "responsive" in campaignNotificationData else None,
                    touchpoint_id=campaignNotificationData["touchpoint_id"]
                )
                print(newCampaignNotification.message_template)
                print(newCampaignNotification.responsive)
                db.session.add(newCampaignNotification)
                db.session.commit()
                db.session.flush()

                return jsonify({'message': f'Nueva notificación con id {newCampaignNotification.notification_id} creada.'})
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500

@app.route("/notification-touchpoints", methods=["GET", "POST"])
def notification_touchpoints():
    match request.method:
        case "POST":
            try:
                notificationTouchpointData = request.get_json()

                newNotificationTouchpoint = NotificationTouchpoint(
                    channel = notificationTouchpointData["channel"],
                    topic = notificationTouchpointData["topic"]
                )

                db.session.add(newNotificationTouchpoint)
                db.session.commit()
                db.session.flush()

                return jsonify({'message': f'Nueva touchpoint con id {newNotificationTouchpoint.touchpoint_id} creado.'})
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            
@app.route("/points-of-interest", methods=["GET", "POST"])
def points_of_interest():
    match request.method:
        case "POST":
            try:
                POIdata = request.get_json()

                args = {
                    "poi_type": POIdata.get("poi_type"),
                    "poi_name": POIdata.get("poi_name"),
                    "poi_description": POIdata.get("poi_description"),
                    "latitude": POIdata.get("latitude"),
                    "longitude": POIdata.get("longitude"),
                }

                newPOI = PointOfInterest(**args)

                db.session.add(newPOI)
                db.session.commit()
                db.session.flush()

                return jsonify({'message': f'Nuevo POI con id {newPOI.poi_id} creado.'})
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500