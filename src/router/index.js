import { createBrowserRouter } from 'react-router-dom'
import Pdf from '../pages/Pdf'

const router = createBrowserRouter([

  {
    path: '/',
    element: <Pdf />,
  },
])


export default router