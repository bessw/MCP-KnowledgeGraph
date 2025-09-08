import random
import re
import string
import yaml
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

def generate_password(length=16):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def load_config():
    """Load the configuration from config.yaml."""
    with open("config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def save_config(config):
    """Save the updated configuration to config.yaml."""
    with open("config.yaml", "w", encoding="utf-8") as file:
        yaml.dump(config, file)

def get_neo4j_major_version(session):
    """Return Neo4j major version as int, or None if it can't be determined."""
    try:
        result = session.run("CALL dbms.components() YIELD versions RETURN head(versions) AS version")
        record = result.single()
        if record and record.get("version"):
            version = record["version"]
            m = re.match(r"(\d+)\.", version)
            if m:
                return int(m.group(1))
    except Exception:
        return None
    return None

def setup_roles(uri, admin_user, admin_password):
    """Set up roles and users in the Neo4j database."""
    config = load_config()

    # Generate random passwords for the users
    readonly_password = generate_password()
    write_password = generate_password()

    # Connect to the Neo4j database
    driver = GraphDatabase.driver(uri, auth=(admin_user, admin_password))
    try:
        with driver.session() as session:
            # determine server version to decide whether to use granular GRANT syntax
            neo4j_major = get_neo4j_major_version(session)

            # Read user names from the configuration
            readonly_user = config['neo4j']['read_only']['username']
            write_user = config['neo4j']['write']['username']

            # Check if Read-Only User exists
            result = session.run("SHOW USERS;")
            users = [list(record.values())[0] for record in result]
            if readonly_user not in users:
                # Create Read-Only User
                session.run("""
                    CREATE USER $readonly_user SET PASSWORD $password CHANGE NOT REQUIRED;
                """, readonly_user=readonly_user, password=readonly_password)

                # Check if Read-Only Role exists before dropping
                result = session.run("SHOW ROLES;")
                roles = [list(record.values())[0] for record in result]
                if "kg_readonly_role" in roles:
                    session.run("DROP ROLE kg_readonly_role;")

                # Create Read-Only Role and assign granular permissions when supported
                session.run("CREATE ROLE kg_readonly_role")
                if neo4j_major and neo4j_major >= 5:
                    try:
                        # Grant database access
                        session.run("GRANT ACCESS ON DATABASE * TO kg_readonly_role")
                        # Grant read access to nodes and relationships
                        session.run("GRANT MATCH {*} ON GRAPH * NODE * TO kg_readonly_role")
                        session.run("GRANT MATCH {*} ON GRAPH * RELATIONSHIP * TO kg_readonly_role")
                        print("Applied readonly grants for Neo4j 5+.")
                    except Neo4jError as e:
                        print(f"Failed to apply readonly grants: {e}")
                session.run("GRANT ROLE kg_readonly_role TO $readonly_user", readonly_user=readonly_user)

            # Check if Write User exists
            if write_user not in users:
                # Create Write User
                session.run("""
                    CREATE USER $write_user SET PASSWORD $password CHANGE NOT REQUIRED;
                """, write_user=write_user, password=write_password)

                # Check if Write Role exists before dropping
                result = session.run("SHOW ROLES;")
                roles = [list(record.values())[0] for record in result]
                if "kg_write_role" in roles:
                    session.run("DROP ROLE kg_write_role;")

                # Create Write Role and assign granular permissions when supported
                session.run("CREATE ROLE kg_write_role")
                if neo4j_major and neo4j_major >= 5:
                    try:
                        # Grant database access
                        session.run("GRANT ACCESS ON DATABASE * TO kg_write_role")
                        # Grant full write access to the graph
                        session.run("GRANT WRITE ON GRAPH * TO kg_write_role")
                        print("Applied write grants for Neo4j 5+.")
                    except Neo4jError as e:
                        print(f"Failed to apply write grants: {e}")
                session.run("GRANT ROLE kg_write_role TO $write_user", write_user=write_user)
    finally:
        driver.close()

    # Update the config with the new passwords
    config['neo4j']['read_only']['password'] = readonly_password
    config['neo4j']['write']['password'] = write_password
    save_config(config)

    print("Setup complete. Users and roles have been configured.")

if __name__ == "__main__":
    import getpass

    # Load configuration
    config = load_config()
    uri = config['neo4j']['host']

    # Prompt for admin credentials
    admin_user = input("Enter Neo4j admin username: ")
    admin_password = getpass.getpass("Enter Neo4j admin password: ")

    # Run the setup
    setup_roles(uri, admin_user, admin_password)
