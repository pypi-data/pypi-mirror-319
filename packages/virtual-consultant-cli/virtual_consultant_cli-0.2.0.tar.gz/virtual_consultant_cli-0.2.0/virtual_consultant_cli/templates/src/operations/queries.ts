import { Project } from '@wasp/entities'
import { GetProjects } from '@wasp/queries/types'

export const getProjects: GetProjects<void, Project[]> = async (args, context) => {
  if (!context.user) {
    throw new Error('Not authorized')
  }

  return context.entities.Project.findMany({
    where: {
      userId: context.user.id
    },
    orderBy: {
      createdAt: 'desc'
    }
  })
} 