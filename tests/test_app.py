from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ok'
    assert 'app' in data


def test_generate_brief():
    payload = {
        'topic': 'AI for investor research',
        'audience': 'startup founders',
        'goal': 'Prioritize the next 90 days',
        'focus_areas': ['market demand', 'product differentiation', 'risk mitigation'],
        'sources': ['user interviews', 'competitor review', 'public trend data'],
    }

    response = client.post('/api/research/brief', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'title' in data
    assert 'executive_summary' in data
    assert isinstance(data['key_findings'], list)
    assert isinstance(data['recommendations'], list)
