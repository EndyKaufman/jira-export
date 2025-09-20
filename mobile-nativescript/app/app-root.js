import { Observable, Dialogs } from '@nativescript/core';

function createViewModel() {
    const viewModel = new Observable();
    
    // Функция для показа уведомления
    viewModel.showHelloNotification = function() {
        Dialogs.alert({
            title: "Уведомление",
            message: "Привет мир!",
            okButtonText: "OK"
        });
    };

    return viewModel;
}

export function onNavigatingTo(args) {
    const page = args.object;
    page.bindingContext = createViewModel();
}