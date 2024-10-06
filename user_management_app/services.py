class FileUploadService:
    @staticmethod
    def profile_picture_path(instance, filename):
        dot = filename.rfind(".")
        return f"profile_pictures/{instance.user.id}{filename[dot:]}"

    @staticmethod
    def story_attachement_path(instance, filename):
        dot = filename.rfind(".")
        return f"story_attachements/{instance.user.id}/{instance.id}{filename[dot:]}"  # Keeps the file extension

    @staticmethod
    def message_attachement_path(instance, filename):
        dot = filename.rfind(".")
        return f"chat_attachments/{instance.sender.id}/{instance.id}{filename[dot:]}"
