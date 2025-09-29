import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ToolsView() {
  return (
    <div className="p-6">
      <Card>
        <CardHeader>
          <CardTitle>Analysis Tools</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Tools for variant analysis, CRISPR design, and sequence alignment will be available here in the future.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}