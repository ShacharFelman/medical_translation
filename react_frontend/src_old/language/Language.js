class Language{
    labels = {
        textInputPlaceholder:{
            eng:"הקלד כאן...",
            heb:"הקלד כאן..."
        },
        translationText:{
            eng:"Translation",
            heb:"תרגום"
        },   
        textText:{
            eng:"Text",
            heb:"טקסט"
        },
        settingsText:{
            eng:"Settings",
            heb:"הגדרות"
        },
        generateText:{
            eng:"Translate All",
            heb:"תרגם הכל"
        },
        translateText:{
            eng:"Translate",
            heb:"תרגם"
        },

        referenceFileLabelText:{
            eng:"Reference File:",
            heb:":קובץ ייחוס"
        },
        noFileSelectedText:{
            eng:"No file selected",
            heb:"קובץ לא נבחר"
        },
        hebrewText:{
            eng:"Hebrew",
            heb:"עברית"

        },
        englishText:{
            eng:"English",
            heb:"אנגלית"
        },
        languageText:{
            eng:"language",
            heb:"שפה"
        },
        headerText:{
            eng:"Drug Leaflets Translation",
            heb:"תרגום עלוני תרופות"
        },
        supportedFilesText:{
            eng:"Supported file types: Docs, PDF",
            heb: "DOC, PDF "+ " סוגי קבצים הנתמכים"
        } ,


        fileNotFoundText:{
            eng:"File not found",
            heb:"קובץ לא נמצא"
        },

        dragAndDropFileText:{
            eng:"Drag And drop your files",
            heb:"גרור קובץ ושחרר"
        },
        browseFilesText:{
            eng:"Browse file",
            heb:"בחר קובץ"
        },
        orText:{
            eng:"OR",
            heb:"או"
        },
        successfullReferenceUploadText:{
            eng:"reference file uploaded successfuly!",
            heb:"קובץ ייחוס הועלה בהצלחה!"
        },
        pText:{
            eng:"P",
            heb:"פ"
        },
        invalidInputText:{
            eng:"invalid input",
            heb:"טקסט שגוי"
        },
        pleaseEnterTextText:{
            eng:"please enter text",
            heb:"אנא הכנס טקסט"
        },
        referenceFileNotUploadWarningText:{
            eng:"Reference File Was Not Uploaded, Are You Sure You Want To Continue?",
            heb:"?"+"קובץ ייחוס לא הועלה, אתה בטוח שאתה רוצה להמשיך"
        },
        warningText:{
            eng:"Warning",
            heb:"אזהרה"
        },
        continueText:{
            eng:"Continue",
            heb:"המשך"
        },
        cancelText:{
            eng:"Cancel",
            heb:"בטל"

        },
        partText:{
            eng:"Part",
            heb:"חלק"

        },
        successfulCopy: {
            eng:"successfuly copied",
            heb:"הועתק בהצלחה"
        }



    }
    constructor(language) {
        this.language = language;
    }

    setLanguage(language) {
        this.language = language;
    }


    _get_text_by_language(label){
        switch(this.language){
            case "eng":
                return label.eng;
            case "heb":
                return label.heb;
            default:
                throw new Error("unknown language");
        }
    }

    textInputPlaceholder(){
        return this._get_text_by_language(this.labels.textInputPlaceholder);
    }
    translationText(){
        return this._get_text_by_language(this.labels.translationText);
    }
    textText(){
        return this._get_text_by_language(this.labels.textText);
    }
    settingsText(){
        return this._get_text_by_language(this.labels.settingsText);
    }
    generateText(){
        return this._get_text_by_language(this.labels.generateText);
    }
    referenceFileLabelText(){
        return this._get_text_by_language(this.labels.referenceFileLabelText);
    }
    noFileSelectedText(){
        return this._get_text_by_language(this.labels.noFileSelectedText);   
    }
    hebrewText(){
        return this._get_text_by_language(this.labels.hebrewText);   
    }
    englishText(){
        return this._get_text_by_language(this.labels.englishText);   
    }
    languageText(){
        return this._get_text_by_language(this.labels.languageText);   
    }
    headerText(){
        return this._get_text_by_language(this.labels.headerText);   
    }
    supportedFilesText(){
        return this._get_text_by_language(this.labels.supportedFilesText);   
    }


    fileNotFoundText(){
        return this._get_text_by_language(this.labels.fileNotFoundText);   
    }
    dragAndDropFileText(){
        return this._get_text_by_language(this.labels.dragAndDropFileText);   
    }
    browseFilesText(){
        return this._get_text_by_language(this.labels.browseFilesText);   
    }

    orText(){
        return this._get_text_by_language(this.labels.orText);   
    }
    successfullReferenceUploadText(){
        return this._get_text_by_language(this.labels.successfullReferenceUploadText);   
    }

    translateText(){
        return this._get_text_by_language(this.labels.translateText);   
    }

    pText(){
        return this._get_text_by_language(this.labels.pText);   
    }
    invalidInputText(){
        return this._get_text_by_language(this.labels.invalidInputText);   
    }
    pleaseEnterTextText(){
        return this._get_text_by_language(this.labels.pleaseEnterTextText);
    }
    referenceFileNotUploadWarningText(){
        return this._get_text_by_language(this.labels.referenceFileNotUploadWarningText);
    }
    warningText(){
        return this._get_text_by_language(this.labels.warningText);
    }
    continueText(){
        return this._get_text_by_language(this.labels.continueText);
    }
    cancelText(){
        return this._get_text_by_language(this.labels.cancelText);
    }
    
    partText(){
        return this._get_text_by_language(this.labels.partText);
    }

    successfulCopy(){
        return this._get_text_by_language(this.labels.successfulCopy);
    }
    
    
    

    
}

export default Language;
