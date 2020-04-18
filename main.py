from app import create_app
from config import ProdConfig

application = create_app(ProdConfig)
application.run(debug=True)
