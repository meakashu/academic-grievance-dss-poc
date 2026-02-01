package com.grievance.model;

import java.util.Map;
import java.util.HashMap;
import java.io.Serializable;

/**
 * Grievance model representing a student's academic grievance submission.
 * This class is used as a fact in the Drools rule engine.
 */
public class Grievance implements Serializable {
    private static final long serialVersionUID = 1L;

    private String id;
    private String studentId;
    private String type;
    private String narrative;
    private Map<String, Object> parameters;

    // Attendance-related fields
    private Double attendancePercentage;
    private Boolean hasMedicalCertificate;
    private Boolean medicalCertificateValid;
    private Boolean medicalCertificateFromRecognizedAuthority;
    private Integer daysAbsent;

    // Examination-related fields
    private String examType;
    private String courseCode;
    private Integer marksObtained;
    private Integer daysSinceResultDeclaration;
    private Boolean hasAlreadyRequestedReeval;
    private Boolean reevaluationFeePaid;
    private Integer nextGradeBoundary;
    private Boolean appealWithin30Days;

    // Fee-related fields
    private String studentCategory;
    private Double familyIncome;
    private Boolean hasIncomeCertificate;
    private Boolean hasCategoryCertificate;
    private Boolean previousInstallmentDefaulted;
    private Double feeAmount;

    // Administrative fields
    private Integer daysDelayed;
    private Boolean transcriptRequestComplete;

    public Grievance() {
        this.parameters = new HashMap<>();
    }

    public Grievance(String id, String studentId, String type, String narrative) {
        this.id = id;
        this.studentId = studentId;
        this.type = type;
        this.narrative = narrative;
        this.parameters = new HashMap<>();
    }

    // Getters and Setters

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getNarrative() {
        return narrative;
    }

    public void setNarrative(String narrative) {
        this.narrative = narrative;
    }

    public Map<String, Object> getParameters() {
        return parameters;
    }

    public void setParameters(Map<String, Object> parameters) {
        this.parameters = parameters;
    }

    // Attendance getters/setters
    public Double getAttendancePercentage() {
        return attendancePercentage;
    }

    public void setAttendancePercentage(Double attendancePercentage) {
        this.attendancePercentage = attendancePercentage;
    }

    public Boolean getHasMedicalCertificate() {
        return hasMedicalCertificate;
    }

    public void setHasMedicalCertificate(Boolean hasMedicalCertificate) {
        this.hasMedicalCertificate = hasMedicalCertificate;
    }

    public Boolean getMedicalCertificateValid() {
        return medicalCertificateValid;
    }

    public void setMedicalCertificateValid(Boolean medicalCertificateValid) {
        this.medicalCertificateValid = medicalCertificateValid;
    }

    public Boolean getMedicalCertificateFromRecognizedAuthority() {
        return medicalCertificateFromRecognizedAuthority;
    }

    public void setMedicalCertificateFromRecognizedAuthority(Boolean medicalCertificateFromRecognizedAuthority) {
        this.medicalCertificateFromRecognizedAuthority = medicalCertificateFromRecognizedAuthority;
    }

    public Integer getDaysAbsent() {
        return daysAbsent;
    }

    public void setDaysAbsent(Integer daysAbsent) {
        this.daysAbsent = daysAbsent;
    }

    // Examination getters/setters
    public String getExamType() {
        return examType;
    }

    public void setExamType(String examType) {
        this.examType = examType;
    }

    public String getCourseCode() {
        return courseCode;
    }

    public void setCourseCode(String courseCode) {
        this.courseCode = courseCode;
    }

    public Integer getMarksObtained() {
        return marksObtained;
    }

    public void setMarksObtained(Integer marksObtained) {
        this.marksObtained = marksObtained;
    }

    public Integer getDaysSinceResultDeclaration() {
        return daysSinceResultDeclaration;
    }

    public void setDaysSinceResultDeclaration(Integer daysSinceResultDeclaration) {
        this.daysSinceResultDeclaration = daysSinceResultDeclaration;
    }

    public Boolean getHasAlreadyRequestedReeval() {
        return hasAlreadyRequestedReeval;
    }

    public void setHasAlreadyRequestedReeval(Boolean hasAlreadyRequestedReeval) {
        this.hasAlreadyRequestedReeval = hasAlreadyRequestedReeval;
    }

    public Boolean getReevaluationFeePaid() {
        return reevaluationFeePaid;
    }

    public void setReevaluationFeePaid(Boolean reevaluationFeePaid) {
        this.reevaluationFeePaid = reevaluationFeePaid;
    }

    public Integer getNextGradeBoundary() {
        return nextGradeBoundary;
    }

    public void setNextGradeBoundary(Integer nextGradeBoundary) {
        this.nextGradeBoundary = nextGradeBoundary;
    }

    public Boolean getAppealWithin30Days() {
        return appealWithin30Days;
    }

    public void setAppealWithin30Days(Boolean appealWithin30Days) {
        this.appealWithin30Days = appealWithin30Days;
    }

    // Fee getters/setters
    public String getStudentCategory() {
        return studentCategory;
    }

    public void setStudentCategory(String studentCategory) {
        this.studentCategory = studentCategory;
    }

    public Double getFamilyIncome() {
        return familyIncome;
    }

    public void setFamilyIncome(Double familyIncome) {
        this.familyIncome = familyIncome;
    }

    public Boolean getHasIncomeCertificate() {
        return hasIncomeCertificate;
    }

    public void setHasIncomeCertificate(Boolean hasIncomeCertificate) {
        this.hasIncomeCertificate = hasIncomeCertificate;
    }

    public Boolean getHasCategoryCertificate() {
        return hasCategoryCertificate;
    }

    public void setHasCategoryCertificate(Boolean hasCategoryCertificate) {
        this.hasCategoryCertificate = hasCategoryCertificate;
    }

    public Boolean getPreviousInstallmentDefaulted() {
        return previousInstallmentDefaulted;
    }

    public void setPreviousInstallmentDefaulted(Boolean previousInstallmentDefaulted) {
        this.previousInstallmentDefaulted = previousInstallmentDefaulted;
    }

    public Double getFeeAmount() {
        return feeAmount;
    }

    public void setFeeAmount(Double feeAmount) {
        this.feeAmount = feeAmount;
    }

    // Administrative getters/setters
    public Integer getDaysDelayed() {
        return daysDelayed;
    }

    public void setDaysDelayed(Integer daysDelayed) {
        this.daysDelayed = daysDelayed;
    }

    public Boolean getTranscriptRequestComplete() {
        return transcriptRequestComplete;
    }

    public void setTranscriptRequestComplete(Boolean transcriptRequestComplete) {
        this.transcriptRequestComplete = transcriptRequestComplete;
    }

    @Override
    public String toString() {
        return "Grievance{" +
                "id='" + id + '\'' +
                ", studentId='" + studentId + '\'' +
                ", type='" + type + '\'' +
                ", attendancePercentage=" + attendancePercentage +
                ", hasMedicalCertificate=" + hasMedicalCertificate +
                '}';
    }
}
