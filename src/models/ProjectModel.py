class ProjectModel:

    def __init__(
        self,
        db_client
    ):

        self.collection = (
            db_client["projects"]
        )


    async def create_project(
        self,
        project_id: str
    ):

        new_project = {

            "project_id": project_id,
        }

        result = (
            await self.collection.insert_one(
                new_project
            )
        )

        new_project["_id"] = (
            result.inserted_id
        )

        return new_project


    async def get_project(
        self,
        project_id: str
    ):

        return await self.collection.find_one({

            "project_id": project_id,
        })


    async def get_project_or_create_one(
        self,
        project_id: str
    ):

        project = await self.get_project(
            project_id
        )

        if project:
            return project

        return await self.create_project(
            project_id
        )


    async def get_all_projects(self):

        projects = []

        async for project in (
            self.collection.find({})
        ):

            projects.append(project)

        return projects