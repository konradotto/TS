/* Copyright (C) 2016 Ion Torrent Systems, Inc. All Rights Reserved */

#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QMainWindow>
#include "RawTab.h"
#include "AlignmentTab.h"
#include "BfMaskTab.h"
#include "WellsTab.h"
#include "NoiseTab.h"
#include "GainTab.h"
#include "NumpyTab.h"
#include "MicroscopeTab.h"


QT_BEGIN_NAMESPACE
class QAction;
class QDialogButtonBox;
class QGroupBox;
class QLabel;
class QLineEdit;
class QMenu;
class QMenuBar;
class QPushButton;
class QTextEdit;
class QComboBox;
QT_END_NAMESPACE

class FileTab;
class RawTab;
class AlignmentTab;
class BfMaskTab;
class NoiseTab;
class GainTab;
class WellsTab;
class NumpyTab;
class MicroscopeTab;

//! [0]
class Dialog : public QMainWindow //QDialog
{
    Q_OBJECT

public:
    Dialog();
    int GetRawExpmt_Y(){return RawExpmt_Y;}
    int GetRawExpmt_X(){return RawExpmt_X;}



private:
    void AutoCompletePaths();

    QString RawExpmtDir="";
    QString OutputDir="";
    int RawExpmt_X=-1;
    int RawExpmt_Y=-1;
    int thumbnail = 0;
//    int RawExpmt_W=-1;
//    int RawExpmt_H=-1;

    FileTab *mFileTab;
    RawTab *mRawTab;
    BfMaskTab *mBfMaskTab;
    WellsTab *mWellsTab;
    NoiseTab *mNoiseTab;
    GainTab *mGainTab;
    AlignmentTab *mAlignmentTab;
    NumpyTab *mNumpyTab;
    MicroscopeTab *mMicroscopeTab;
    QString DatFileName="";
    QString BfMaskFileName="";
    QString NoiseFileName="";
    QString GainFileName="";
    QString WellsFileName="";
    QString BamFileName="";
    QString NumpyFileName="";
    QString MicroscopeFileName="";

    QAction *OpenDatAct=NULL;
    QAction *OpenBfMaskAct=NULL;
    QAction *OpenNoiseAct=NULL;
    QAction *OpenGainAct=NULL;
    QAction *OpenWellsAct=NULL;
    QAction *OpenBamAct=NULL;
    QAction *OpenNumpyAct=NULL;
    QAction *OpenMicroscopeAct=NULL;

    private slots:
        void about();
        void browseDatDir();
        void browseBfMaskDir();
        void browseNoiseDir();
        void browseGainDir();
        void browseWellsDir();
        void browseBamDir();
        void browseNumpyDir();
        void browseMicroscopeDir();
        void currentChanged(int index);
        void Clear();
        void Save();
    	void fileNameChanged(QString fname);

};
//! [0]



#endif // DIALOG_H
