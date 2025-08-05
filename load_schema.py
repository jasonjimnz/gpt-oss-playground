import psycopg2


def main():
    """Main function to run the script."""
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="banking_db"
    )
    with conn.cursor() as cursor:
        cursor.execute(
            open('./ddl/schema.sql', encoding='utf-8').read()
        )
        cursor.connection.commit()
    print("Generated schema")
    conn.close()


if __name__ == "__main__":
    main()
