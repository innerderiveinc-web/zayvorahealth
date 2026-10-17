"use client";

import React from "react";
import DoctorWorkspacePage from "../page";

export default function DoctorPatientDynamicPage({
  params,
}: {
  params: { patientId: string };
}) {
  return <DoctorWorkspacePage initialPatientId={params.patientId} />;
}
