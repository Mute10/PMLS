 #http://localhost:8000/docs
from fastapi import FastAPI, Header, Depends, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Project, Base 
from schematics import ProjectCreate, Project as ProjectPydantic
from tools import SessionLocal, engine
import crud
from crud import update_project

app = FastAPI()
Base.metadata.create_all(bind=engine)

def verify_token(x_token: str = Header(...)):
    if x_token != "supersecrettoken":
        raise HTTPException(status_code = 401, detail ="Invalid token")
    
# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/metrics") #where do i use limit, offset and queries?
def get_matrics(db: Session = Depends(get_db)):
    total = db.query(Project).count()
    last_updated = db.query(Project).order_by(Project.update_at_desc().first())
    return {"total_projects": total, "last_updated": last_updated.updated_at if last_updated else None}

@app.post("/projects", summary = " ", operation_id="createProjects", response_model=ProjectPydantic)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.get("/projects", summary=" ", operation_id="getProjects",response_model=list[ProjectPydantic])
def read_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)

@app.get("/projects/{project_id}", summary=" ", operation_id="getProjects", response_model = ProjectPydantic)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code = 404, detail = "Project Not Found")
    return project

@app.put("/projects/{project_id}", summary=" ", operation_id="updateProject", response_model = ProjectPydantic)
def update_project_by_id(project_id: int, project_data: ProjectCreate, db: Session = Depends(get_db)):
    updated = update_project(db, project_id, project_data)
    if updated is None:
        raise HTTPException(status_code = 404, detail = "Project not found")
    return updated

@app.delete("/projects/{project_id}", summary=" ", response_model=dict)
def delete_project_by_id(project_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail = "Project not found")
    return {"message": "Project deleted successfully"}

#root endpoint
@app.get("/root", summary = " ", operation_id="getRoot")
def read_root():
 return {"message": "Project Management Lifecycle System is live"}








globalSolution = (33, 300, 0.30)

class CurrentStatus:
    def __init__(self, time, budget):
        self.time = time 
        self.budget = budget
    def businessSolution(overtime):
        annualSalary, OT, jrPay = 150000, 30, 60000
        result = 0
        if OT > jrPay:
            jrPay += (OT * 8)
            annualSalary += (OT * 8)
            result += (annualSalary + jrPay)
        else:
            OT -= OT
            result -= (annualSalary - jrPay)
        return result

class Goals(CurrentStatus):
    def __init__(self, time, budget, strategy):
        super().__init__(time, budget)
        self.strategy = strategy
    def supplyChains(cocaCola, brewery):
        result = 0
        supplyCount = 0
        global globalSolution
        newSolution = globalSolution + (99,)
        for c in range(len(cocaCola)):
            for b in range(len(brewery)):
                if cocaCola >  brewery:
                    supplyCount += 2
                    cocaCola.pop()
                    brewery.pop()
                    result += supplyCount
                else:
                    pass
            return supplyCount
        return result
    supplyChains([1,2,1,2,1,2], [12, 12, 12, 15])      



Goals(12, 30900, "waterfall")
CurrentStatus("well", "great")

class Objectives:
    project_team = {"Mike Taktarov" : "Vice President of Operations",
                        "Patrick Kruzchev" : "Project Mangager",
                        "Jesse Frederick" : "Jr. Project Manager",
                        "Brad Wolf" : "IT Support Specialist",
                        "Fumiko Takushima" : "Sony Tech Support"

                       }