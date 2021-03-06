#! /usr/bin/python
#-*- coding:utf-8 -*

import os
import glob
import shutil

import conf
from web.models import Shelter, Category, ShelterPicture
from bootstrap import db

#! /usr/bin/python
#-*- coding:utf-8 -*

import os
import glob
import shutil

import conf
from web.models import Shelter, Category, ShelterPicture
from bootstrap import db

def import_shelters_pictures(folder):
    shelters = Shelter.query.all()

    for shelter in shelters:
        shelter_rid = shelter.get_values_of_attribute(attribute_name='ID')[0].name
        print("Shelter_rid '{}' ...".format(shelter_rid))
			
        for picture in glob.glob(folder + shelter_rid + '/**.jpg'):
            picture_name = os.path.basename(picture)
            print("Picture name '{}' ...".format(picture_name))
            
            try:
                category_name = picture_name.split('_')[1]
                picture_subject = os.path.splitext(picture_name.split('_')[2])[0]
            except:
                print("failed")
                continue

            print("Picture subject '{}' ...".format(picture_subject))
            print("Category name '{}' ...".format(category_name))
            category = Category.query.filter(Category.name==category_name,
                                    Category.parent_id!=None).first()

            if category:
                if picture_subject.lower() == 'facade':
                    new_picture = ShelterPicture(file_name=picture_name,
                                    shelter_id=shelter.id,
                                    category_id=category.id,
                                    is_main_picture=True)
                else:
                    new_picture = ShelterPicture(file_name=picture_name,
                                    shelter_id=shelter.id,
                                    category_id=category.id)

                db.session.add(new_picture)
                db.session.commit()

                path = os.path.join(conf.SHELTERS_PICTURES_SERVER_PATH,
                                                            str(shelter.id))
                if not os.path.exists(path):
                    os.makedirs(path)

                shutil.copy(picture, path)
                print("Copy from '{}' ...".format(picture))
                print("Copy to '{}' ...".format(path))
