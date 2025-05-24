import { test, expect } from '@playwright/test';

test('scenario1: search for חיים לוינסון and verify results', async ({ page }) => {
  // Scenario step 1: please open @https://haaretz.co.il/
  console.log('Navigating to haaretz.co.il...');
  await page.goto('https://haaretz.co.il/');
  
  // Wait for page to load (initial wait)
  console.log('Waiting 10 seconds for initial page load...');
  await page.waitForTimeout(10000);
  console.log('Initial page load wait complete.');
  
  // Scenario step 2: click on the search button up left
  console.log('Locating search button...');
  const searchButton = page.getByTestId('search-btn');
  console.log('Found search button:', await searchButton.count(), 'elements');
  if (await searchButton.count() > 0) {
    console.log('Search button visible:', await searchButton.isVisible());
  } else {
    console.log('Search button not found!');
    await page.pause();
    return;
  }
  
  console.log('Clicking search button...');
  await searchButton.click();
  console.log('Clicked search button.');

  // Scenario step 3: type 'חיים לוינסון' at the search input
  console.log('Locating search input by placeholder...');
  const searchInput = page.getByPlaceholder('הקלידו לחיפוש באתר');
  
  console.log('Waiting for search input to be visible...');
  await searchInput.waitFor({ state: 'visible', timeout: 10000 });
  // .fill() and .press() will auto-wait for enabled, so explicit check removed
  console.log('Search input is visible.');

  console.log('Found search input:', await searchInput.count(), 'elements');
  if (await searchInput.count() === 0) {
    console.log('Search input not found!');
    const html = await page.content(); // page.content() is correct for full page HTML
    console.log('Current page HTML:', html.substring(0, 2000)); // Log a portion
    await page.pause(); 
    return; 
  }

  console.log('Filling search input with: חיים לוינסון');
  await searchInput.fill('חיים לוינסון');
  console.log('Search input filled.');
  
  console.log('Pressing Enter on search input...');
  await searchInput.press('Enter');
  console.log('Pressed Enter on search input.');

  // Scenario step 4: output the top one (top search result)
  console.log('Waiting a few seconds for search results to load...');
  await page.waitForTimeout(5000); // Give an explicit few seconds for results to appear
  
  console.log('Locating search results container using data-testid="Marco-list"...');
  const searchResultsContainer = page.getByTestId('Marco-list');
  await searchResultsContainer.waitFor({ state: 'visible', timeout: 20000 }); 
  console.log('Search results container is visible.');

  console.log('Locating search result articles within the container...');
  const results = searchResultsContainer.locator('article[data-testid="marco-list-teaser"]');
  console.log('Found', await results.count(), 'search results items.');
  
  if (await results.count() > 0) {
    const firstResult = results.first();
    
    console.log('--- First Search Result ---');
    const firstResultHTML = await firstResult.innerHTML(); 
    console.log('HTML (first 500 chars):', firstResultHTML.substring(0,500));
    
    // Title is in h3 > a (based on provided HTML)
    const titleElement = firstResult.locator('h3 a');
    let title = 'N/A';
    if (await titleElement.count() > 0) {
      title = await titleElement.first().innerText();
    }
    console.log('Title:', title);
    
    // Link is the href of the first <a> tag, a direct child of the article or within the h3
    const linkElement = firstResult.locator('a[href]').first(); // Get the first <a> with an href
    let link = 'N/A';
    if (await linkElement.count() > 0) {
      link = (await linkElement.getAttribute('href')) || 'N/A'; 
    }
    console.log('Link:', link);
    console.log('-------------------------');

  } else {
    console.log('No search results found with the specified selectors.');
    const pageHTML = await page.content(); 
    console.log('Current page HTML for debugging results not found (first 5000 chars):', pageHTML.substring(0, 5000));
  }
  
  console.log('Test finished. Pausing for 20 seconds to allow inspection...');
  await page.waitForTimeout(20000);
});
