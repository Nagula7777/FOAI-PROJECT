import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Download } from 'lucide-react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { reportApi } from '../services/financialService';
import apiClient from '../services/apiClient';

export default function MonthlyReportsPage() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = () => reportApi.list().then(setReports);
  useEffect(() => { load(); }, []);

  const generate = async () => {
    setLoading(true);
    await reportApi.generate();
    await load();
    setLoading(false);
  };

  const downloadPdf = async (id, month) => {
    const response = await apiClient.get(reportApi.pdfUrl(id), { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.download = `report-${month}.pdf`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Monthly Reports</h1>
        <button type="button" className="btn-primary" onClick={generate} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Report'}
        </button>
      </div>
      <DisclaimerBanner />
      <div className="space-y-3">
        {reports.map((r) => (
          <div key={r.id} className="card flex items-center justify-between">
            <div>
              <Link to={`/reports/${r.id}`} className="font-semibold text-brand-700">{r.report_month}</Link>
              <p className="text-sm text-slate-500">Health score: {r.health_score}/100</p>
            </div>
            <button type="button" onClick={() => downloadPdf(r.id, r.report_month)} className="btn-secondary gap-2">
              <Download className="h-4 w-4" /> PDF
            </button>
          </div>
        ))}
        {!reports.length && <p className="text-sm text-slate-500">No reports yet. Generate your first monthly report.</p>}
      </div>
    </div>
  );
}
