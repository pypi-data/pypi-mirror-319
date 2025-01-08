import { Project } from '@wasp/entities'
import { CreateProject } from '@wasp/actions/types'

type CreateProjectInput = Pick<Project, 'name' | 'description'>

export const createProject: CreateProject<CreateProjectInput, Project> = async (args, context) => {
  if (!context.user) {
    throw new Error('Not authorized')
  }

  const project = await context.entities.Project.create({
    data: {
      name: args.name,
      description: args.description,
      user: {
        connect: {
          id: context.user.id
        }
      }
    }
  })

  return project
} 