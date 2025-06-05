function displayMessage(message, type, chatBox) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);
    if (type === 'bot') {
        messageElement.innerHTML = marked.parse(message); 
    } else {
        messageElement.textContent = message;
    }
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

export function displaySourceDocuments(sourceDocs, chatBox) {
    if (sourceDocs && sourceDocs.length > 0) {
        const sourceDocContainer = document.createElement('div');
        sourceDocContainer.classList.add('source-documents');

        const heading = document.createElement('h4');
        heading.textContent = 'Source Documents:';
        sourceDocContainer.appendChild(heading);

        const toggleButton = document.createElement('button');
        toggleButton.classList.add('source-toggle-button');
        toggleButton.textContent = 'Show Source Documents';
        sourceDocContainer.appendChild(toggleButton);

        const sourceDocsContent = document.createElement('div');
        sourceDocsContent.classList.add('source-documents-content');
        sourceDocsContent.style.display = 'none'; // Hidden by default

        sourceDocs.forEach((doc, index) => {
            const docElement = document.createElement('div');
            docElement.classList.add('source-document-item');

            const title = document.createElement('h5');
            const fileName = doc.metadata && doc.metadata.source ? doc.metadata.source.split('/').pop() : `Document ${index + 1}`;
            const pageNumber = doc.metadata && doc.metadata.page !== undefined ? ` (Page ${doc.metadata.page + 1})` : '';
            title.textContent = `${fileName}${pageNumber}`;
            docElement.appendChild(title);

            const content = document.createElement('p');
            content.classList.add('source-document-content');
            let fullText = doc.page_content;

            // Process the text to only keep newlines if preceded by a period
            fullText = fullText.replace(/(?<!\.)\r?\n/g, ' ');

            const lines = fullText.split(/\r\n|\r|\n/);
            const maxLines = 5;
            const truncatedText = lines.length > maxLines
                ? lines.slice(0, maxLines).join('\n') + '...'
                : fullText;

            content.textContent = truncatedText;
            content.dataset.fullText = fullText;
            content.dataset.truncatedText = truncatedText;
            docElement.appendChild(content);

            if (lines.length > maxLines) {
                const expandButton = document.createElement('button');
                expandButton.classList.add('expand-button');
                expandButton.textContent = 'Read more';
                expandButton.addEventListener('click', () => {
                    if (content.textContent === truncatedText) {
                        content.textContent = fullText;
                        expandButton.textContent = 'Show less';
                    } else {
                        content.textContent = truncatedText;
                        expandButton.textContent = 'Read more';
                    }
                    chatBox.scrollTop = chatBox.scrollHeight;
                });
                docElement.appendChild(expandButton);
            }

            sourceDocsContent.appendChild(docElement); // Append to new content div
        });

        sourceDocContainer.appendChild(sourceDocsContent); // Add content div to main container

        toggleButton.addEventListener('click', () => {
            if (sourceDocsContent.style.display === 'none') {
                sourceDocsContent.style.display = 'block';
                toggleButton.textContent = 'Hide Source Documents';
            } else {
                sourceDocsContent.style.display = 'none';
                toggleButton.textContent = 'Show Source Documents';
            }
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom after expanding/collapsing
        });

        chatBox.appendChild(sourceDocContainer);
    }
}

async function processStreamedResponse(reader, chatBox) {
    const decoder = new TextDecoder('utf-8');
    let fullResponse = '';
    let botMessageElement = null;
    let sourceDocuments = [];
    let isReadingSourceDocs = false;
    let sourceDocsBuffer = '';

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });

        if (chunk.includes('SOURCE_DOCUMENTS_START') && chunk.includes('SOURCE_DOCUMENTS_END')) {
            sourceDocsBuffer = chunk.split('SOURCE_DOCUMENTS_START')[1].split('SOURCE_DOCUMENTS_END')[0];
            try {
                sourceDocuments = JSON.parse(sourceDocsBuffer);
                displaySourceDocuments(sourceDocuments, chatBox);
            } catch (e) {
                console.error('Error parsing source documents:', e);
            }
            break;
        } else if (chunk.includes('SOURCE_DOCUMENTS_START')) {
            isReadingSourceDocs = true;
            sourceDocsBuffer = chunk.split('SOURCE_DOCUMENTS_START')[1];
            continue;
        } else if (chunk.includes('SOURCE_DOCUMENTS_END')) {
            sourceDocsBuffer += chunk.split('SOURCE_DOCUMENTS_END')[0];
            try {
                sourceDocuments = JSON.parse(sourceDocsBuffer);
                displaySourceDocuments(sourceDocuments, chatBox);
            } catch (e) {
                console.error('Error parsing source documents:', e);
            }
            break;
        }
        if (isReadingSourceDocs) {
            sourceDocsBuffer += chunk;
        } else {
            if (!botMessageElement) {
                botMessageElement = document.createElement('div');
                botMessageElement.classList.add('message', 'bot');
                chatBox.appendChild(botMessageElement);
            }
            fullResponse += chunk;
            botMessageElement.innerHTML = marked.parse(fullResponse);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
}
