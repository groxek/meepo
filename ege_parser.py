import asyncio
from playwright.async_api import async_playwright
from database import AsyncSessionLocal
from models import Task, Subject
from sqlalchemy.future import select

ANSWERS = [
    "21", "52,5", "3,6", "129", "36", "0,28", "77", "46", "0,96", "17",
    "7", "10", "17", "10", "200", "18", "168", "60", "4704", "40",
    "30", "87", "242", "152", "0,3", "0,25", "0,3", "0,6", "0,3", "0,9",
    "0,1", "0,02", "0,56", "5", "0,22", "0,79", "0,0625", "0,2", "0,192", "0,5",
    "-5", "-4", "1", "3", "-5", "1", "7", "-4", "1", "2",
    "-3,1", "11", "2", "1", "4", "23", "-1", "6", "7", "7",
    "26", "-4", "4", "4", "12", "6000", "90", "24", "55", "0,25",
    "5", "0,48", "20", "65", "342", "17", "16", "3", "480", "45",
    "2", "8", "15", "-29", "-16", "122", "64", "-17", "3", "8",
    "-6", "10", "32", "4", "-1", "20"
]

async def run_parser():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Subject).where(Subject.name == "Профильная математика"))
        subject = result.scalars().first()
        if not subject:
            subject = Subject(name="Профильная математика")
            session.add(subject)
            await session.commit()
            await session.refresh(subject)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(
                "https://math-ege.sdamgia.ru/test?id=92036162&nt=True&pub=False",
                wait_until="domcontentloaded",
                timeout=60000
            )
            
            await page.wait_for_selector(".prob_maindiv")
            tasks = await page.locator(".prob_maindiv").all()
            
            for i, task_node in enumerate(tasks):
                condition_locator = task_node.locator(".pbody").first
                
                images = await condition_locator.locator("img").all()
                img_urls = []
                for img in images:
                    src = await img.get_attribute("src")
                    if src:
                        if "formula/svg" in src:
                            continue 
                        if src.startswith("/"):
                            src = "https://math-ege.sdamgia.ru" + src
                        img_urls.append(src)
                
                condition_html = await condition_locator.evaluate('''
                    (node) => {
                        let clone = node.cloneNode(true);
                        let imgs = clone.querySelectorAll('img');
                        imgs.forEach(img => {
                            let src = img.getAttribute('src') || '';
                            if (src.startsWith('/')) {
                                img.setAttribute('src', 'https://math-ege.sdamgia.ru' + src);
                            }
                            
                            if (img.getAttribute('src').includes('formula/svg')) {
                                img.style.height = '1.3em';
                                img.style.verticalAlign = 'middle';
                                img.style.display = 'inline-block';
                                img.style.margin = '0 4px';
                                img.style.filter = 'invert(1) brightness(1.5)';
                            } else {
                                img.remove();
                            }
                        });
                        return clone.innerHTML.trim();
                    }
                ''')
                
                clean_answer = ANSWERS[i] if i < len(ANSWERS) else "Ответа нет"
                
                db_task = Task(
                    subject_id=subject.id,
                    question=condition_html,
                    answer=clean_answer,
                    images=img_urls
                )
                session.add(db_task)
                
            await session.commit()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_parser())