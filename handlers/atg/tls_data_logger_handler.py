t into the given data stream
        :note: a serialized object would ``_deserialize`` into the same object
        :param stream: a file-like object
        :return: self"""
        raise NotImplementedError("To be implemented in subclass")

    def _deserialize(self,