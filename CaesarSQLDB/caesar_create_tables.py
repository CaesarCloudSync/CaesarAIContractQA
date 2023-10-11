class CaesarCreateTables:
    def __init__(self) -> None:
        self.contractfields = ("filename","contractfile","filetype")
        self.questionfields = ("filename","question","filetype")

    def create(self,caesarcrud):
        caesarcrud.create_table("contractid",self.contractfields,
        ("varchar(255) NOT NULL","MEDIUMBLOB NOT NULL","varchar(255) NOT NULL"),
        "contracts")
        caesarcrud.create_table("questiond",self.questionfields,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL"),
        "questions")
