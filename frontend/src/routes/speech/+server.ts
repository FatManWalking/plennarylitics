// import { json } from '@sveltejs/kit';
import { postContent } from '$lib/services/backend';
import { json } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function GET() {
	
	const speechesJSON = await getContent(`/speeches`); //TODO: add filters

	return json(projectJSON);
}