document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('research-form');
  const loading = document.getElementById('loading');
  const resultTitle = document.getElementById('result-title');
  const executiveSummary = document.getElementById('executive-summary');
  const keyFindings = document.getElementById('key-findings');
  const risks = document.getElementById('risks');
  const recommendations = document.getElementById('recommendations');
  const actionPlan = document.getElementById('action-plan');

  const renderList = (element, values) => {
    element.innerHTML = '';
    values.forEach((value) => {
      const item = document.createElement('li');
      item.textContent = value;
      element.appendChild(item);
    });
  };

  const renderOrderedList = (element, values) => {
    element.innerHTML = '';
    values.forEach((value) => {
      const item = document.createElement('li');
      item.textContent = value;
      element.appendChild(item);
    });
  };

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    loading.classList.remove('hidden');

    const formData = new FormData(form);
    const payload = {
      topic: formData.get('topic') || '',
      audience: formData.get('audience') || '',
      goal: formData.get('goal') || '',
      focus_areas: (formData.get('focus_areas') || '')
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
      sources: (formData.get('sources') || '')
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
    };

    try {
      const response = await fetch('/api/research/brief', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Request failed');
      }

      const data = await response.json();
      resultTitle.textContent = data.title || 'Research brief';
      executiveSummary.textContent = data.executive_summary || 'No executive summary available.';
      renderList(keyFindings, data.key_findings || []);
      renderList(risks, data.risks || []);
      renderList(recommendations, data.recommendations || []);
      renderOrderedList(actionPlan, data.action_plan || []);
    } catch (error) {
      resultTitle.textContent = 'Brief generation failed';
      executiveSummary.textContent = 'The system could not generate a brief right now. Please try again in a moment.';
      renderList(keyFindings, []);
      renderList(risks, []);
      renderList(recommendations, []);
      renderOrderedList(actionPlan, []);
    } finally {
      loading.classList.add('hidden');
    }
  });
});
