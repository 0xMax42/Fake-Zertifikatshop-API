from backend.models import Product, Stock
from backend.database import get_session, init_db
from sqlmodel import select

def seed_products():
    init_db()

    with get_session() as session:
        # Check if there are already products in the database        
        existing = session.exec(select(Product)).all()
        if existing:
            print("Products already exist in the database. Skipping seeding.")
            return

        # List of example product tuples: (name, short_desc, full_desc, stock_quantity, price)
        products = [
            ("Meister der Kaffeetrinkerei", "Für unermüdliche Bürosklaven",
             "Dieses Zertifikat bestätigt, dass du pro Tag mindestens 3 Kaffee trinkst.", 10, 15.99),
            ("Prokrastinier-Experte", "Für Aufschieberitis-Profis",
             "Bescheinigt dir das größte Talent, Dinge auf morgen zu verschieben.", 20, 12.50),
            ("Power-Nap-Ninja", "Für Kurzschläfer-Könige",
             "Ausgestellt für alle, die 10-Minuten-Schläfchen zur Kunstform machen.", 7, 18.00),
            ("Meeting-Überlebender", "Für Sitzungs-Veteranen",
             "Bestätigt, dass du mindestens 50 sinnlose Meetings überlebt hast.", 5, 20.00),
            ("Excel-Zauberer", "Für Tabellenkünstler",
             "Dieses Zertifikat ehrt deine Fähigkeit, Excel-Tabellen mit Magie zu füllen.", 15, 17.49)
        ]

        for name, short_desc, full_desc, quantity, price in products:
            product = Product(
                name=name,
                short_description=short_desc,
                product_description=full_desc,
                price=price
            )
            session.add(product)
            session.flush()  # ensure product.id is available

            stock = Stock(quantity=quantity, product_id=product.id)
            session.add(stock)

        session.commit()
        print("Products seeded successfully.")

if __name__ == "__main__":
    seed_products()
