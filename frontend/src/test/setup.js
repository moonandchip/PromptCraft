import '@testing-library/jest-dom/vitest'
import { vi } from 'vitest'

vi.mock('/vite.svg', () => ({
  default: '/vite.svg',
}))
