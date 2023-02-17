import { postContent } from '$lib/services/backend';
import { json } from '@sveltejs/kit';


// This is the function that is called when the user submits the form
// It is called by the search button in src/routes/speech/+page.svelte
// Need to use POST because the backend will return a error using a body otherwise
/** @type {import('./$types').RequestHandler} */
export async function POST(filters: object) {
	
	const speechesJSON = await postContent(`/speeches`, filters);

	return json(speechesJSON);
}