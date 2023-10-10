class CaesarCreateTables:
    def __init__(self) -> None:
        self.contractfields = ("filename","contractfile","filetype")
        self.questionfields = ("filename","question")

    def create(self,caesarcrud):
        caesarcrud.create_table("contractid",self.contractfields,
        ("varchar(255) NOT NULL","MEDIUMBLOB","MEDIUMBLOB"),
        "contracts")
