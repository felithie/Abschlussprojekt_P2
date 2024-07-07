import json
import os

class Person:
    def __init__(self, name, username, age):
        self.name = name
        self.username = username
        self.age = int(age)
        self.attributes = {}
        
    def add_attribute(self, key, value):
        self.attributes[key] = value
        
    def save_to_json(self, filename=None):
        if filename is None:
            filename = f"{self.username}.json"
        data = {
            'name': self.name,
            'username': self.username,
            'age': self.age,
            'attributes': self.attributes
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
        
    @classmethod
    # load_from_json() ist eine Klassenmethode, die ein neues Person-Objekt aus einer JSON-Datei erstellt.
    def load_from_json(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        person = cls(data['name'], data['username'], data['age'])
        person.attributes = data['attributes']
        return person
    
    def calculatemaxhr(self):
        return 220 - self.age

def main():
    username = input("Geben Sie den Benutzername ein: ")
    filename = f"{username}.json"
    
    if os.path.exists(filename):
        person = Person.load_from_json(filename)
        print(f"Willkommen zurück, {person.name}!")
    else:
        name = input("Geben Sie Ihren Namen ein: ")
        age = input("Geben Sie Ihr Alter ein: ")
        person = Person(name, username, int(age))
    
    while True:
        action = input("Möchten Sie ein neues Attribut hinzufügen? (ja/nein): ")
        if action.lower() == 'ja':
            key = input("Geben Sie den Namen des Attributs ein: ")
            value = input("Geben Sie den Wert des Attributs ein: ")
            person.add_attribute(key, value)
        else:
            break
    
    person.save_to_json(filename)
    print("Daten wurden gespeichert.")
    
if __name__ == "__main__":
    main()
