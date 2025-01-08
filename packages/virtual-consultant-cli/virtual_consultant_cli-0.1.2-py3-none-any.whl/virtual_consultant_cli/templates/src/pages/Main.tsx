import React from 'react'
import { useQuery } from '@wasp/queries'
import { useAction } from '@wasp/actions'
import getProjects from '@wasp/queries/getProjects'
import createProject from '@wasp/actions/createProject'

const MainPage = () => {
  const { data: projects, isLoading, error } = useQuery(getProjects)
  const createProjectFn = useAction(createProject)

  if (isLoading) return 'Loading...'
  if (error) return 'Error: ' + error

  const handleCreateProject = () => {
    createProjectFn({
      name: 'New Project',
      description: 'A new Virtual Consultant project'
    })
  }

  return (
    <div className='p-4'>
      <h1 className='text-4xl font-bold mb-8'>Virtual Consultant</h1>
      
      <div className='mb-8'>
        <button
          onClick={handleCreateProject}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
        >
          Create New Project
        </button>
      </div>

      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
        {projects.map((project: any) => (
          <div
            key={project.id}
            className='border rounded-lg p-4 hover:shadow-lg transition-shadow'
          >
            <h2 className='text-xl font-semibold mb-2'>{project.name}</h2>
            <p className='text-gray-600'>{project.description}</p>
            <div className='mt-4 text-sm text-gray-500'>
              Created: {new Date(project.createdAt).toLocaleDateString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default MainPage 