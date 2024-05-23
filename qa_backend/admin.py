# admin.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from flask_cors import cross_origin

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/documents/set-access', methods=['POST'])
@cross_origin()  # Allows CORS requests to this endpoint from any origin
def set_document_access():
    from app import db
    from models import User, DocumentAccess  # Import the User model
    data = request.get_json()
    doc_id = data['doc_id']
    status = data['status']

    if status in ['enabled', 'disabled']:
        access_right = True if status == 'enabled' else False
        # Update existing records
        DocumentAccess.query.filter_by(doc_id=doc_id).update({'access_right': access_right})
        # Ensure all users have a corresponding entry
        all_users = User.query.all()
        existing_access_users = [access.user_id for access in DocumentAccess.query.filter_by(doc_id=doc_id).all()]
        for user in all_users:
            if user.user_id not in existing_access_users:
                new_access = DocumentAccess(doc_id=doc_id, user_id=user.user_id, access_right=access_right)
                db.session.add(new_access)
        db.session.commit()
    return jsonify({"message": f"Document access set to {status}"}), 200

@admin_bp.route('/documents/access/refresh', methods=['GET'])
@cross_origin()  # Allows CORS requests to this endpoint from any origin
def refresh_access_status():
    from app import db
    from models import Document  # Import the User model
    documents = Document.query.all()
    documents_data = [
        {
            "doc_id": doc.doc_id,
            "doc_name": doc.doc_name,
            "access_status": doc.get_access_status(),  # Use the refined method
            "uploader_name": doc.txt_uploader_name
        }
        for doc in documents
    ]
    return jsonify(documents_data), 200

@admin_bp.route('/user-documents/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_documents(user_id):
    from app import db
    from models import DocumentAccess, User, Document
    try:
            # Check if the user exists to handle invalid user IDs
            if not User.query.get(user_id):
                return jsonify({"error": "User not found"}), 404
            
            # Get all documents
            all_documents = Document.query.all()
            
            # Get existing access for the user
            existing_access = {access.doc_id: access for access in DocumentAccess.query.filter_by(user_id=user_id)}
            
            # Prepare the result list including documents the user has no explicit access to
            result = []
            for document in all_documents:
                if document.doc_id in existing_access:
                    access = existing_access[document.doc_id]
                    doc_info = {
                        "doc_id": access.doc_id,
                        "has_access": access.access_right,
                        "doc_name": document.doc_name,
                        "uploader_name": document.txt_uploader_name,
                        "create_time": document.txt_createtime
                    }
                else:
                    # Assume 'false' access if no record exists
                    doc_info = {
                        "doc_id": document.doc_id,
                        "has_access": False,
                        "doc_name": document.doc_name,
                        "uploader_name": document.txt_uploader_name,
                        "create_time": document.txt_createtime
                    }
                result.append(doc_info)

            return jsonify(result), 200
    except Exception as e:
        # Log the exception
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@admin_bp.route('/user-documents/access', methods=['POST'])
@cross_origin()  # Allows CORS requests to this endpoint from any origin
def modify_user_document_access():
    from app import db
    from models import DocumentAccess  # Import the User model
    data = request.get_json()
    user_id = data['user_id']
    doc_id = data['doc_id']
    access_right = data['access_right']

    # Retrieve the existing access entry, if it exists
    access = DocumentAccess.query.filter_by(user_id=user_id, doc_id=doc_id).first()
    
    if access:
        access.access_right = access_right
    else:
        # If no existing access, create a new access entry
        access = DocumentAccess(user_id=user_id, doc_id=doc_id, access_right=access_right)
        db.session.add(access)
    
    db.session.commit()
    return jsonify({"message": "Document access updated successfully"}), 200


# @admin_bp.route('/document-access', methods=['GET', 'POST'])
# @login_required
# def document_access():
#     from app import db
#     if not current_user.is_admin:
#         return jsonify({"message": "Unauthorized"}), 403

#     if request.method == 'POST':
#         data = request.get_json()
#         doc_id = data.get('doc_id')
#         enable = data.get('enable', True)  # True to enable, False to disable

#         # Update the document access in the database
#         result = db.documents.update_one({'_id': doc_id}, {'$set': {'enabled': enable}})
#         if result.modified_count:
#             return jsonify({"message": "Document access updated"}), 200
#         else:
#             return jsonify({"message": "No changes made or document not found"}), 404

#     # For GET request, return the list of all documents
#     documents = db.documents.find()
#     return jsonify([doc for doc in documents]), 200
