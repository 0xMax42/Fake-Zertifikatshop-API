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
             "Dieses Zertifikat ehrt deine Fähigkeit, Excel-Tabellen mit Magie zu füllen.", 15, 17.49),
            ("Kaffee-Jongleur", "Meistert 3 Kaffees gleichzeitig",
            "Dieses Zertifikat bescheinigt, dass du fähig bist, 3 Kaffeebecher gleichzeitig zu balancieren – ohne einen Tropfen zu verschütten.", 12, 9.99),
            ("To-Do-Listen-Titan", "Erstellt Listen in Listen in Listen",
            "Für diejenigen, die es lieben, Aufgabenlisten für Aufgabenlisten zu machen.", 30, 8.50),
            ("Mikrowellen-Magier", "Zauberer des schnellen Aufwärmens",
            "Dieses Zertifikat verleiht dir die Macht, jedes Gericht in unter 2 Minuten aufzuwärmen – mit Präzision und Stil.", 18, 11.11),
            ("Multitasking-Meister", "Arbeitet an 5 Projekten gleichzeitig",
            "Bescheinigt, dass du mindestens 5 Browser-Tabs offen hast und alle gleichzeitig bedienen kannst.", 25, 13.33),
            ("Copy-Paste-König", "Copy & Paste in Perfektion",
            "Dieses Zertifikat ehrt deine unvergleichliche Fähigkeit, Code und Texte von StackOverflow zu kopieren und wie neu aussehen zu lassen.", 40, 7.77)
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
