{{/*
This file contains a bunch of Helm Go template "functions" that can be used
throughout the chart and help make things DRY.
*/}}

{{/*
Expand the name of the chart.
*/}}
{{- define "chipy-k8s.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "chipy-k8s.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create name of the secret that we can use in secrets.yaml and anywhere that
the secret is used.
*/}}
{{- define "chipy-k8s.secret" -}}
{{- (include "chipy-k8s.fullname" .) }}
{{- end }}


{{/*
Create name of the PVC that we can use in pvc.yaml and anywhere that
the PVC is used.
*/}}
{{- define "chipy-k8s.pvc" -}}
{{- (include "chipy-k8s.fullname" .) }}
{{- end }}

{{/*
Create name of the job-collectstatic
*/}}
{{- define "chipy-k8s.job-collectstatic" -}}
{{- (include "chipy-k8s.fullname" .) }}-collectstatic
{{- end }}

{{/*
Create name of the job-migrate
*/}}
{{- define "chipy-k8s.job-migrate" -}}
{{- (include "chipy-k8s.fullname" .) }}-migrate
{{- end }}

{{/*
Create name of the job-superuser
*/}}
{{- define "chipy-k8s.job-superuser" -}}
{{- (include "chipy-k8s.fullname" .) }}-superuser
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "chipy-k8s.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "chipy-k8s.labels" -}}
helm.sh/chart: {{ include "chipy-k8s.chart" . }}
{{ include "chipy-k8s.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "chipy-k8s.selectorLabels" -}}
app.kubernetes.io/name: {{ include "chipy-k8s.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "chipy-k8s.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "chipy-k8s.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
