        ct = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        class_name = ''
        if 'self' in frame.f_locals:
            class_name = frame.f_locals["self"].__class__.__name__
        is_fs_writing = func_name == 'save' and class_name == 'FileStorage'
        if 'password' in new_dict and not is_fs_writing:
            del new_dict['password']
        return new_dict


    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
