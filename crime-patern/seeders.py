from app import app
from models import *

# regions = [    'Arusha',    'Dar-es-Salaam',    'Dodoma',    'Geita',    'Iringa',    'Kagera',    'Katavi',    'Kigoma',    'Kilimanjaro',    'Lindi',    'Manyara',    'Mara',    'Mbeya',    'Morogoro',    'Mtwara',    'Mwanza',    'Njombe',    'Pemba North',    'Pemba South',    'Pwani',    'Rukwa',    'Ruvuma',    'Shinyanga',    'Simiyu',    'Singida',    'Songwe',    'Tabora',    'Tanga',    'Unguja North',    'Unguja South',    'Zanzibar Central/South']

regions = ['ARUSHA','DAR-ES-SALAAM','DODOMA','GEITA','IRINGA','KAGERA','KATAVI','KIGOMA','KILIMANJARO','LINDI','MANYARA','MARA','MBEYA','MOROGORO','MTWARA','MWANZA,','NJOMBE','PWANI','RUKWA','RUVUMA','SHINYANGA','SIMIYU','SINGIDA','SONGWE','TABORA','TANGA']

#regions = [s.upper() for s in regions]

crime = ['MURDER','RAPE','CHILD_DESERTION','UNNATURAL_OFFENCE','DEFILEMENT']
for region in regions:
    loc = Location(name=region)
 
    with app.app_context():

        db.session.add(loc)
        
        db.session.commit()
with app.app_context():       
 result = Location.query.filter_by(name='Dar-es-Salaam').first() 
      
user = User(fullname='rex',username='rsiphael@gmail.com',phoneNumber='0655594998',is_admin=True,location_id=result.id)
user.set_password('12345')
  
with app.app_context():

        db.session.add(user)
        
        db.session.commit()


for crime in crime:
    crim = CrimeType(name=crime)
    
    with app.app_context():

        db.session.add(crim)
        
        db.session.commit()   
     
#print(a)    
#db.session.add_all(a)
