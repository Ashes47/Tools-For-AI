from pydantic import BaseModel


# Define the BrowsingRequest model
class BraveSearchRequest(BaseModel):
    topic: str

    class Config:
        json_schema_extra = {"example": {"topic": "Quantum Computing"}}


class BraveSearchResult(BaseModel):
    titles: list[str]
    links: list[str]
    descriptions: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "titles": [
                    "What is Quantum Computing? | IBM",
                    "Quantum computing - Wikipedia",
                    "Quantum computers are like kaleidoscopes − why unusual metaphors help illustrate science and technology",
                    "What is Quantum Computing? - Quantum Computing Explained - AWS",
                ],
                "links": [
                    "https://www.ibm.com/topics/quantum-computing",
                    "https://en.wikipedia.org/wiki/Quantum_computing",
                    "https://theconversation.com/quantum-computers-are-like-kaleidoscopes-why-unusual-metaphors-help-illustrate-science-and-technology-228178",
                    "https://aws.amazon.com/what-is/quantum-computing/",
                ],
                "descriptions": [
                    "<strong>Quantum</strong> <strong>computing</strong> is a rapidly-emerging technology that harnesses the laws of <strong>quantum</strong> mechanics to solve problems too complex for classical <strong>computers</strong>.",
                    "A <strong>quantum</strong> <strong>computer</strong> is a <strong>computer</strong> that exploits <strong>quantum</strong> mechanical phenomena. On small scales, physical matter exhibits properties of both particles and waves, and <strong>quantum</strong> <strong>computing</strong> leverages this behavior using specialized hardware. Classical physics cannot explain the operation of these <strong>quantum</strong> ...",
                    "Novel metaphors can make it easier to understand complex concepts such as <strong>quantum</strong> <strong>computing</strong>.",
                    "Find out what is <strong>Quantum</strong> <strong>Computing</strong> and how to use Amazon Web Services for <strong>Quantum</strong> <strong>Computing</strong>",
                ],
            }
        }
