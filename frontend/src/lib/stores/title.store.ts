import { writable } from 'svelte/store';

// initialize with the light theme, dawn
const title = writable('Plannarilytics')

export { title };