from pymongo.collection import Collection
from config import client

class ArtGalleryDB:

    def __init__(self):
        self.gallery_col = Collection(client['ArtGalley'], 'likes data')
        
    def find(self, data):
        return self.gallery_col.find_one(data)

    def add(self, data):
        self.gallery_col.insert_one(data)

    def modify(self, search_dict, new_dict):
        try:
            self.gallery_col.find_one_and_update(search_dict, {'$set': new_dict})
        except Exception as e:
            print(f"Exception in ArtGAlleryDB -> modify\n\n{e}")
