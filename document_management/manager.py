import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import mimetypes

class DocumentManager:
    """Manage document uploads, storage, validation, and retrieval (Mock version - no database)"""
    
    # Class-level storage for mock data (persists across instances)
    _mock_documents = {}
    _document_id_counter = 1
    
    def __init__(self, db_host=None, db_name=None, db_user=None, db_pass=None, storage_path="documents"):
        self.storage_path = storage_path
        self.local_storage_dir = os.path.join(storage_path, "local")
        
        # Create storage directories
        os.makedirs(self.local_storage_dir, exist_ok=True)
        
        # Allowed file types
        self.allowed_formats = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
        self.max_file_size_mb = 10  # Default 10MB
    
    def validate_file(self, file_path: str, max_size_mb: int = None) -> Tuple[bool, str]:
        """
        Validate file format and size
        
        Returns: (is_valid, error_message)
        """
        if max_size_mb is None:
            max_size_mb = self.max_file_size_mb
        
        # Check if file exists
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File size ({file_size_mb:.2f}MB) exceeds limit ({max_size_mb}MB)"
        
        # Check file extension
        file_extension = Path(file_path).suffix.lower().lstrip('.')
        if file_extension not in self.allowed_formats:
            return False, f"File format .{file_extension} not allowed. Allowed: {', '.join(self.allowed_formats)}"
        
        return True, ""
    
    def upload_document(self, request_id: int, user_id: int, file_path: str, 
                       document_type_id: int = None, expiry_days: int = 365) -> Dict:
        """
        Upload and store document (Mock version)
        
        Args:
            request_id: Service request ID
            user_id: User uploading the document
            file_path: Path to the file to upload
            document_type_id: Type of document (optional)
            expiry_days: Days until document expires (default 1 year)
        
        Returns: Dictionary with upload result
        """
        try:
            # Validate file
            is_valid, error_msg = self.validate_file(file_path)
            if not is_valid:
                return {"success": False, "message": error_msg}
            
            # Get file info
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_extension = Path(file_path).suffix.lower().lstrip('.')
            
            # Create organized storage path
            storage_subpath = f"req_{request_id}/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
            destination_path = os.path.join(self.local_storage_dir, storage_subpath)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy file to storage
            shutil.copy2(file_path, destination_path)
            
            # Calculate expiry date
            expiry_date = datetime.now() + timedelta(days=expiry_days)
            
            # Store in mock storage
            document_id = DocumentManager._document_id_counter
            DocumentManager._document_id_counter += 1
            
            DocumentManager._mock_documents[document_id] = {
                "id": document_id,
                "request_id": request_id,
                "document_type_id": document_type_id,
                "user_id": user_id,
                "file_name": file_name,
                "file_path": destination_path,
                "file_type": file_extension,
                "file_size_bytes": file_size,
                "storage_type": "local",
                "expiry_date": expiry_date.isoformat(),
                "status": "active",
                "upload_date": datetime.now().isoformat(),
                "is_verified": False,
                "verified_by": None,
                "verified_at": None
            }
            
            return {
                "success": True,
                "document_id": document_id,
                "file_name": file_name,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "storage_path": destination_path,
                "expiry_date": expiry_date.isoformat(),
                "message": "Document uploaded successfully"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Upload failed: {str(e)}"}
    
    
    def get_document(self, document_id: int) -> Optional[Dict]:
        """Get document details by ID (Mock version)"""
        return DocumentManager._mock_documents.get(document_id)
    
    def download_document(self, document_id: int) -> Optional[str]:
        """Get file path for download"""
        doc = self.get_document(document_id)
        if doc and os.path.exists(doc['file_path']):
            return doc['file_path']
        return None
    
    def get_request_documents(self, request_id: int) -> List[Dict]:
        """Get all documents for a service request (Mock version)"""
        documents = []
        for doc in DocumentManager._mock_documents.values():
            if doc['request_id'] == request_id and doc['status'] == 'active':
                file_size_mb = round(doc['file_size_bytes'] / (1024 * 1024), 2)
                if file_size_mb < 1:
                    file_size_formatted = f"{round(doc['file_size_bytes'] / 1024, 2)} KB"
                else:
                    file_size_formatted = f"{file_size_mb} MB"
                
                documents.append({
                    "id": doc['id'],
                    "file_name": doc['file_name'],
                    "file_type": doc['file_type'],
                    "file_size_mb": file_size_mb,
                    "file_size_formatted": file_size_formatted,
                    "upload_date": doc['upload_date'],
                    "is_verified": doc['is_verified'],
                    "status": doc['status'],
                    "document_type_id": doc['document_type_id']
                })
        
        return sorted(documents, key=lambda x: x['upload_date'], reverse=True)
    
    def verify_document(self, document_id: int, verified_by_user_id: int) -> Dict:
        """Mark document as verified (Mock version)"""
        if document_id in DocumentManager._mock_documents:
            DocumentManager._mock_documents[document_id]['is_verified'] = True
            DocumentManager._mock_documents[document_id]['verified_by'] = verified_by_user_id
            DocumentManager._mock_documents[document_id]['verified_at'] = datetime.now().isoformat()
            return {"success": True, "message": "Document verified"}
        return {"success": False, "message": "Document not found"}
    
    def delete_document(self, document_id: int) -> Dict:
        """Delete/archive document (Mock version)"""
        if document_id in DocumentManager._mock_documents:
            doc = DocumentManager._mock_documents[document_id]
            
            # Delete from filesystem
            if os.path.exists(doc['file_path']):
                try:
                    os.remove(doc['file_path'])
                except:
                    pass
            
            # Mark as deleted
            DocumentManager._mock_documents[document_id]['status'] = 'deleted'
            return {"success": True, "message": "Document deleted"}
        return {"success": False, "message": "Document not found"}
    
    def cleanup_expired_documents(self) -> Dict:
        """Delete expired documents (Mock version)"""
        deleted_count = 0
        current_time = datetime.now()
        
        for doc_id, doc in DocumentManager._mock_documents.items():
            if doc['status'] == 'active':
                expiry_date = datetime.fromisoformat(doc['expiry_date'])
                if expiry_date <= current_time:
                    try:
                        if os.path.exists(doc['file_path']):
                            os.remove(doc['file_path'])
                        DocumentManager._mock_documents[doc_id]['status'] = 'archived'
                        deleted_count += 1
                    except:
                        pass
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Cleaned up {deleted_count} expired documents"
        }
    
    def get_storage_stats(self) -> Dict:
        """Get document storage statistics (Mock version)"""
        total_docs = 0
        total_size = 0
        storage_by_type = {}
        format_data = {}
        
        for doc in DocumentManager._mock_documents.values():
            if doc['status'] == 'active':
                total_docs += 1
                total_size += doc['file_size_bytes']
                
                # Count by storage type
                storage_type = doc['storage_type']
                if storage_type not in storage_by_type:
                    storage_by_type[storage_type] = {"count": 0, "size": 0}
                storage_by_type[storage_type]["count"] += 1
                storage_by_type[storage_type]["size"] += doc['file_size_bytes']
                
                # Count by file type
                file_type = doc['file_type']
                if file_type not in format_data:
                    format_data[file_type] = {"count": 0, "size": 0}
                format_data[file_type]["count"] += 1
                format_data[file_type]["size"] += doc['file_size_bytes']
        
        # Format storage by type
        storage_by_type_list = []
        for storage_type, data in storage_by_type.items():
            storage_by_type_list.append({
                "storage_type": storage_type,
                "count": data["count"],
                "total_size_mb": round(data["size"] / (1024*1024), 2)
            })
        
        # Format by file type
        format_data_list = []
        for file_type, data in format_data.items():
            format_data_list.append({
                "file_type": file_type,
                "count": data["count"],
                "total_size_mb": round(data["size"] / (1024*1024), 2)
            })
        
        return {
            "total_documents": total_docs,
            "total_size_gb": round(total_size / (1024*1024*1024), 2),
            "avg_file_size_mb": round((total_size / (1024*1024)) / max(total_docs, 1), 2),
            "by_storage_type": storage_by_type_list,
            "by_file_type": format_data_list
        }
